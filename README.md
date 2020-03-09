This project is used to visualize my net worth over time.
It currently only supports importing First Calgary Credit Union exported statements.
The statements must have been exported in (Oldest to newest) mode.
Statements should be in CSV format inside `statements/`
Then theoretically one would run main.py

It is currently not working correctly because my plot needs to fill in balances for days that don't have one.
The bank only exports transactions, so any day without a transaction has an unknown balance. It must therefore be
carried over from a previous day or derived to be $0. This is in-progress during the refactoring.



## Versions
- dbe72a5e38b6aa189199866938ff6a0641c9b7ca: Before refactor
