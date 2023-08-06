"""A small utility to create mortgage schedules for beancount."""

import argparse
from decimal import Decimal
from dataclasses import dataclass
import datetime

from dateutil.relativedelta import relativedelta

__version__ = "0.2"


@dataclass
class MortgagePayment:
    """A payment event in a mortgage."""

    payee: str
    date: datetime.date
    description: str
    payment: Decimal
    interests: Decimal
    principal_paid: Decimal
    outstanding_principal: Decimal

    def to_beancount_lines(
        self,
        currency: str,
        liability_account: str,
        assets_account: str,
        fees_account: str,
    ) -> str:
        """Return the balances of the transaction for Beancount."""
        description_line = (
            f'{self.date.isoformat()} ! "{self.payee}" "{self.description}"'
        )
        payment_entry = f"  {assets_account:<30}    {-self.payment} {currency}"
        fees_entry = f"  {fees_account:<30}    {self.interests} {currency}"
        liability_entry = (
            f"  {liability_account:<30}    {self.principal_paid} {currency}"
        )
        balance_check = f"{self.date.isoformat()} balance {liability_account} {-self.outstanding_principal} {currency}"
        return "\n".join(
            [
                description_line,
                payment_entry,
                fees_entry,
                liability_entry,
                "\n",
                balance_check,
            ]
        )


@dataclass
class Mortgage:
    """A mortgage."""

    payee: str
    description: str
    first_payment_date: datetime.date
    principal: Decimal
    duration: Decimal
    rate_yearly: Decimal

    def fixed_payment_schedule(self) -> [MortgagePayment]:
        """Reimbursement schedule with fixed monthly payment constraint."""
        outstanding = self.principal
        ret = []
        monthly_payment = fixed_monthly_payment(
            self.principal, self.rate_yearly, self.duration
        )
        for i in range(0, int(self.duration.to_integral_value()) - 1):
            fees = interests(outstanding, self.rate_yearly)
            capital_paid = monthly_payment - fees
            outstanding = outstanding - capital_paid
            ret.append(
                MortgagePayment(
                    payee=self.payee,
                    date=self.first_payment_date + relativedelta(months=i),
                    description=f"{self.description} - payment {i+1}",
                    payment=monthly_payment,
                    interests=fees,
                    principal_paid=capital_paid,
                    outstanding_principal=outstanding,
                )
            )
        # Unrolling last iteration because the payment is going to be different
        fees = interests(outstanding, self.rate_yearly)
        if fees + outstanding > monthly_payment:
            # This means the last payment covers a duration longer than necessary.
            # We change the fees to match the last payment
            fees = monthly_payment - outstanding
        assert (
            fees + outstanding
        ) <= monthly_payment, (
            "the last payment must be less than or equal to the fixed payment."
        )
        ret.append(
            MortgagePayment(
                payee=self.payee,
                date=self.first_payment_date + relativedelta(months=self.duration - 1),
                description=f"{self.description} - payment {self.duration}",
                payment=fees + outstanding,
                interests=fees,
                principal_paid=outstanding,
                outstanding_principal=Decimal(0),
            )
        )
        return ret


def fixed_monthly_payment(
    principal: Decimal, rate_yearly: Decimal, duration_months: Decimal
) -> Decimal:
    """Return the fixed monthly payment for the given loan."""
    rate_monthly = rate_yearly / Decimal(12)
    return (
        principal
        * rate_monthly
        * ((Decimal(1) + rate_monthly) ** duration_months)
        / (((Decimal(1) + rate_monthly) ** duration_months) - 1)
    ).quantize(Decimal("1.00"))


def interests(outstanding_principal: Decimal, rate_yearly: Decimal) -> Decimal:
    """Return the fixed monthly payment for the given loan."""
    rate_monthly = rate_yearly / Decimal(12)
    return (outstanding_principal * rate_monthly).quantize(Decimal("1.00"))


def outstanding_loan_balance(
    principal: Decimal,
    rate_yearly: Decimal,
    duration_months: Decimal,
    months_paid: Decimal,
) -> Decimal:
    """Return the outstanding due principal after a given amount of months paid."""
    rate_monthly = rate_yearly / Decimal(12)
    return (
        principal
        * (
            ((Decimal(1) + rate_monthly) ** duration_months)
            - ((Decimal(1) + rate_monthly) ** months_paid)
        )
        / (((Decimal(1) + rate_monthly) ** duration_months) - 1)
    ).quantize(Decimal("1.00"))


def main():
    """Run the CLI utility."""
    parser = argparse.ArgumentParser(
        prog="bean-mortgage",
        description="Print a beancount-formatted mortgage/loan schedule.",
        epilog="Don't forget to double check the amounts with the schedule your lender gave you.",
    )
    parser.add_argument(
        "principal",
        type=str,
        help="Total principal amount of the loan",
    )
    parser.add_argument(
        "duration",
        type=int,
        help="Duration of the loan in months",
    )
    parser.add_argument(
        "rate",
        type=str,
        help="Yearly rate of the loan",
    )
    parser.add_argument(
        "-c",
        "--commodity",
        type=str,
        help="Commodity to use for the loan",
        default="EUR",
    )
    parser.add_argument(
        "-l",
        "--liability",
        type=str,
        help="Liability account to put the loan on",
        default="Liabilities:Mortgage",
    )
    parser.add_argument(
        "-e",
        "--expense",
        type=str,
        help="Expenses account to charge the interests to",
        default="Expenses:Fees:Mortgage-Interest",
    )
    parser.add_argument(
        "-a",
        "--asset",
        type=str,
        help="Asset to take the payments from",
        default="Assets:Bank:Account",
    )
    parser.add_argument(
        "-p",
        "--payee",
        type=str,
        help="Payee for the loan reimbursements",
        default="Banque de France",
    )
    parser.add_argument(
        "-d",
        "--description",
        type=str,
        help="Description to put for the loan",
        default="Mortgage",
    )
    parser.add_argument(
        "-f",
        "--first-payment",
        type=str,
        help="Date of the first payment in ISO format",
        default=datetime.date.today().isoformat(),
    )

    args = parser.parse_args()

    rate = Decimal(args.rate)
    principal = Decimal(args.principal)
    duration = Decimal(args.duration)
    mortgage = Mortgage(
        args.payee,
        args.description,
        datetime.date.fromisoformat(args.first_payment),
        principal,
        duration,
        rate,
    )
    for i, payment in enumerate(mortgage.fixed_payment_schedule()):
        print(
            f"{payment.to_beancount_lines(args.commodity, args.liability, args.asset, args.expense)}\n"
        )


if __name__ == "__main__":
    main()
