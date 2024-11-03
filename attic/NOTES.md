# Asyncronous Input Event Messages
- {fieldname, data}
- comes in "at random times" (i.e. async) with above pair of strings
## Examples
### textarea
input data = a pair of strings, fieldname, data
### button
input data = a pair of strings, buttonname, "pushed"

# Output Messages
- {fieldname, command, data}
## Examples
### Output readonly textarea
output data = 3 strings, fieldname, "update", data
