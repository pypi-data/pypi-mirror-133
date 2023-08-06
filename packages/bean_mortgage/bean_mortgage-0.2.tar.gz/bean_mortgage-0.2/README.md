# Bean Mortage

Simple CLI tool to produce a mortgage schedule for beancount.

`pip install bean_mortgage`

## Example

``` sh
bean-mortgage 150000.00 120 0.0180 \
-c EUR \
-l Liabilities:Mortgage:Island \
-e Expenses:Fees:Mortgage:Island \
-a Assets:Bank:Checking \
-p "Banque de France" \
-d "Loan Island" \
-f 2018-03-19
```

Typically I put this in a separate file for each loan, and I edit the file as
the operations actually happen; and in the main file I put the initial
transaction, which could be in this example:

```
2018-02-20 * "M NotShadyGuy" "Got an island"
  Assets:Island                150000.00 EUR
  Liabilities:Mortgage:Stuff  -150000.00 EUR
```
