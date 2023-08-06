# cccalculator
calculate the cyclomatic complexity of python source file
Use M = E − N + 2 to calculate the complexity .
The output is the McCabe complexity of each python source file under the path.
# Example
cd into the cccalculate directory

$ python calculate.py /path_to_your_python_file_directory/

The output will be like this

/path_to_your_python_file_directory/test_file4.py

   fun:7----------6

/path_to_your_python_file_directory/test_file1.py

   class:1--fun:2----------1

   class:1--fun:5----------5

   fun:26----------5

