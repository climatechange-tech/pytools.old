**NOTICE**

* As of Mon Apr 16 2024 this project has been discontinued.
  
* The reason is that the project was in need of major improvements:
  - Automatic module importations, eliminating:
    - Need of creating a program to set the repository's local directory up.    
      This program created another one at the specified directory when 
      asking for it, which contains a function that returns thereof. 
      It is currently stored at the same directory where this README 
      is located at.
    - As a consequence of the previous point, need of implementing a snippet
      based on 'Path' and 'sys' modules in order to register the repository's
      local directory in every single module.
  - Huge level-up computation performance
  - Unification of case usages
  - Elimination of redundant conditional and instantiation instructions
  - Possible incorporation of OOP

* The first inner point itself does not directly imply OOP, because it is enough
  to add an empty __init__.py program within each directory.
  However, the last inner point implies possible future major restructuration.
* Before discontinuation, this project has been updated to the latest changes
  that include all but the first and last inner points.
* In order to avoid conflicts and maintain the references, this project has been
  renamed to *pytools.old*, in favour of creating the classically named and leveled-up *pytools* repo
