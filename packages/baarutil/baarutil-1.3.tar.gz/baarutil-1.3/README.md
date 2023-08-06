# Baarutil

**This Custom Library is specifically created for the developers/users who use BAAR. Which is a product of [Allied Media Inc](https://www.alliedmedia.com/).**

<h2>
Authors:
</h2>


**Souvik Roy  [sroy-2019](https://github.com/sroy-2019)**

**Zhaoyu (Thomas) Xu  [xuzhaoyu](https://github.com/xuzhaoyu)**



<h2>
Additional Info:
</h2>

The string structure that follows is a streamline structure that the developers/users follow throughout an automation workflow designed in BAAR:
~~~
"Column_1__=__abc__$$__Column_2__=__def__::__Column_1__=__hello__$$__Column_2__=__world"
~~~

<h2>
Available functions and the examples are listed below:
</h2>

<h3>
1.  read_convert(string), Output Data Type: list of dictionary
</h3>

**Attributes:**

  *i.  **string:** Input String, Data Type = String*

~~~
Input:  "Column_1__=__abc__$$__Column_2__=__def__::__Column_1__=__hello__$$__Column_2__=__world"
Output: [{"Column_1":"abc", "Column_2":"def"}, {"Column_1":"hello", "Column_2":"world"}]
~~~

<h3>
2.  write_convert(input_list), Output Data Type: string
</h3>

**Attributes:**

  *i.  **input_list:** List that contains the Dictionaries of Data, Data Type = List*

~~~
Input:  [{"Column_1":"abc", "Column_2":"def"}, {"Column_1":"hello", "Column_2":"world"}]
Output: "Column_1__=__abc__$$__Column_2__=__def__::__Column_1__=__hello__$$__Column_2__=__world"
~~~

<h3>
3.  string_to_df(string, rename_cols, drop_dupes), Output Data Type: pandas DataFrame
</h3>

**Attributes:**

  *i.  **string:** Input String, Data Type = String*

  *ii. **rename_cols:**  Dictionary that contains old column names and new column names mapping, Data Type = Dictionary, Default Value = {}*

  *iii.  **drop_dupes:** Drop duplicate rows from the final dataframe, Data Type = Bool, Default Value = False*

~~~
Input:  "Column_1__=__abc__$$__Column_2__=__def__::__Column_1__=__hello__$$__Column_2__=__world"
~~~

Output:
<table>
  <thead>
    <tr>
      <th>Column_1</th>
      <th>Column_2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>abc</td>
      <td>def</td>
    </tr>
    <tr>
      <td>hello</td>
      <td>world</td>
    </tr>
  </tbody>
</table>

<h3>
4.  df_to_string(input_df, rename_cols, drop_dupes), Output Data Type: string
</h3>

**Attributes:**

  *i. **input_df:** Input DataFrame, Data Type = pandas DataFrame*

  *ii. **rename_cols:**  Dictionary that contains old column names and new column names mapping, Data Type = Dictionary, Default Value = {}*

  *iii. **drop_dupes:** Drop duplicate rows from the final dataframe, Data Type = Bool, Default Value = False*

Input:
<table>
  <thead>
    <tr>
      <th>Column_1</th>
      <th>Column_2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>abc</td>
      <td>def</td>
    </tr>
    <tr>
      <td>hello</td>
      <td>world</td>
    </tr>
  </tbody>
</table>
  
~~~
Output: "Column_1__=__abc__$$__Column_2__=__def__::__Column_1__=__hello__$$__Column_2__=__world"
~~~

<h3>
5.  df_to_listdict(input_df, rename_cols, drop_dupes), Output Data Type: list
</h3>

**Attributes:**

  *i. **input_df:** Input DataFrame, Data Type = pandas DataFrame*

  *ii. **rename_cols:**  Dictionary that contains old column names and new column names mapping, Data Type = Dictionary, Default Value = {}*

  *iii. **drop_dupes:** Drop duplicate rows from the final dataframe, Data Type = Bool, Default Value = False*

Input:
<table>
  <thead>
    <tr>
      <th>Column_1</th>
      <th>Column_2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>abc</td>
      <td>def</td>
    </tr>
    <tr>
      <td>hello</td>
      <td>world</td>
    </tr>
  </tbody>
</table>

~~~
Output: [{"Column_1":"abc", "Column_2":"def"}, {"Column_1":"hello", "Column_2":"world"}]
~~~

<h3>
6.  decrypt_vault(encrypted_message, config_file), Output Data Type: string
</h3>

**Attributes:**

  *i. **encrypted_message:** Encrypted Baar Vault Data, Data Type = string*

  *ii. **config_file:**  Keys, that needs to be provided by [Allied Media](https://www.alliedmedia.com/).*

  This function can also be called from a Robot Framework Script by importing the baarutil library and using Decrypt Vault keyword. Upon initiation of this fuction, this will set the Log Level of the Robot Framework script to NONE for security reasons. The Developers have to use *Set Log Level    INFO* in the robot script in order to restart the Log.

~~~
Input:  <<Encrypted Text>>
Output: <<Decrypted Text>>
~~~

<h3>
7.  generate_password(password_size, upper, lower, digits, symbols), Output Data Type: string
</h3>

**Attributes:**

  *i. **password_size:** Password Length, Data Type = int, Default Value = 10*

  *ii. **upper:**  Are Uppercase characters required?, Data Type = Bool (True/False), Default Value = True*

  *iii. **lower:**  Are Lowercase characters required?, Data Type = Bool (True/False), Default Value = True*

  *iv. **digits:**  Are Digits characters required?, Data Type = Bool (True/False), Default Value = True*

  *v. **symbols:**  Are Symbols/ Special characters required?, Data Type = Bool (True/False), Default Value = True*

  This function can also be called from a Robot Framework Script by importing the baarutil library and using Generate Password keyword. Upon initiation of this fuction, this will set the Log Level of the Robot Framework script to NONE for security reasons. The Developers have to use *Set Log Level    INFO* in the robot script in order to restart the Log.

~~~
Input (Optional):  <<Password Length>>, <<Uppercase Required?>>, <<Lowercase Required?>>, <<Digits Required?>>, <<Symbols Required?>>
Output: <<Password String>>
~~~