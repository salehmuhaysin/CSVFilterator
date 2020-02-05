# CSVFilterator
Filter CSV file (exclude/include) rows based on predefined rules


# Description
This script recevied both CSV file and YAML file contains predefined rules (can be customed), the purpose of this script to filter the csv file, and for each row matches the whitelist rules will be excluded, and row matches the blacklist rules will included. 
## Example:
If you have a csv (process_list.csv) that contains all the process, and you want to filter the CSV file to exclude the well-known processes (via whitelist rules), also you can use blacklist to enforce including the row even if a whitelist rule match.

# Usage
```
                           
                    _:*///:_                     
                _+*///////////+_                
    ____----*////////////////////**----____    
   *//////////////////////////////////********    
   */////////////////       ////**************    
   *////////////////          /***************    
   *///////////////   /////   ****************    
   *//////////////   /////**   ***************    
   *//////////////   ////***   ***************    
   *//////////////   ///****   ***************    
   *////////////                 *************    
   *////////////    Saleh Bin    *************    
   *////////////     Muhaysin    *************    
   *////////////                 *************    
    *////////********************************     
     */////  github.com/salehmuhaysin  *****      
      *///*********************************             
==========================================================
usage: Python script tool filter CSV files based on predefined ruleset
       [-h] -i FILTER -f CSVFILE [-o OUT_FILE] [-d DELIMITER]

optional arguments:
  -h, --help    show this help message and exit
  -o OUT_FILE   Output csv file (default: <csvfile>-filtered.csv)
  -d DELIMITER  Output CSV file delimiter (default ",")

required arguments:
  -i FILTER     filter file contain YAML filter rule
  -f CSVFILE    CSV file to be filtered
```


The script receive the csv file `-f` to filter it, and the filter rules file `-i`, the output file is `<input-file>-filtered.csv`. Optionally you can specify the output file name via `-o`, the output CSV file delimiter can be specified via `-d`

# Rules
the rules written in yaml format, as following

```yaml
<rule-name>:
  _type: '[whitelist|blacklist]'
  <column-name>:
    condition: '[=|~|^|$|r]'
    values: <value(s)>
```
## Example:
```yaml
rule_SYSTEM_known_path:
  _type: 'whitelist'
  User:
    condition: '='
    values: SYSTEM
  Command Line:
    condition: '~'
    values:
      - Windows\system32\lsass.exe
      - Windows\CCM\CcmExec.exe
      - Windows\system32\SearchIndexer.exe /Embedding
      - Windows\System32\spoolsv.exe
      - Program Files\Realtek\Audio\HDA\RAVBg64.exe
      - Windows\system32\conhost.exe
      - Program Files (x86)\Google\Update\GoogleUpdate.exe
```
### condition
- equal: =
- contain: ~
- starts with: ^
- ends with: $
- regex: r


