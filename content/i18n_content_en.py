"""Terjemahan Inggris untuk materi (urutannya sejajar dengan content/lessons.py, quizzes.py, reference.py, pages.py)."""

# ---------------------------------------------------------------- pelajaran: (judul, isi)
LESSONS_EN = {
"html": [
 ("Introduction to HTML",
  "HTML (HyperText Markup Language) is the markup language that gives a web page its structure. The browser reads tags such as <h1> and <p> and displays them as headings and paragraphs.\n\nEvery HTML document starts with <!DOCTYPE html> and contains <head> for page information and <body> for the visible content."),
 ("Elements, Attributes, and Links",
  "An element consists of an opening tag, content, and a closing tag. Attributes give extra information about an element, such as href on a link or src and alt on an image.\n\nAlways fill in the alt attribute on images so the page is understandable to screen readers and still meaningful if the image fails to load."),
 ("Lists and Tables",
  "Use <ul> for bulleted lists, <ol> for numbered lists, and <li> for each item. Data in rows and columns is built with <table>, <tr> (row), <th> (column heading), and <td> (cell)."),
 ("Forms",
  "Forms collect user input. The <input> element has many types (text, email, password, number), and <label> explains each field. The required attribute makes the browser validate mandatory fields."),
],
"css": [
 ("Introduction to CSS and Selectors",
  "CSS (Cascading Style Sheets) controls how HTML elements look. A CSS rule consists of a selector (what to change) and a declaration block (property: value).\n\nCommon selectors: element name (p), class (.card), and id (#header)."),
 ("Colors and the Box Model",
  "Every element is a layered box: content, padding (inner space), border, and margin (outer space). Understanding the box model helps you control spacing and size precisely.\n\nUse box-sizing: border-box so an element's width already includes its padding and border."),
 ("Layout with Flexbox",
  "Flexbox arranges elements in a row or column with ease. Set display: flex on the container, then control direction (flex-direction), alignment (justify-content, align-items), and spacing (gap)."),
 ("Responsive Design with Media Queries",
  "Media queries apply CSS rules only under certain conditions, such as screen width. In the mobile-first approach, write base styles for phones, then add rules for wider screens."),
],
"javascript": [
 ("Variables and Data Types",
  "JavaScript makes web pages interactive. Use const for values that never change and let for those that do; avoid var. Basic types: string, number, boolean, null, undefined."),
 ("Functions",
  "Functions wrap steps so they can be reused. Arrow functions are a short syntax that is very common in modern JavaScript."),
 ("Arrays and Loops",
  "An array stores many values in order. Methods such as map, filter, and reduce process arrays without writing manual loops."),
 ("The DOM and Events",
  "The DOM is a representation of the HTML page that JavaScript can change. Select elements with querySelector, then attach event listeners to respond to clicks, input, and more."),
],
"python": [
 ("Hello Python: Variables and Input/Output",
  "Python is known for its clean syntax. Variables are created directly with =, without type declarations. Use print() to display output and input() to read user input."),
 ("Conditionals and Loops",
  "if/elif/else chooses a program path based on conditions. for repeats over a sequence of data, while repeats as long as a condition is true. Mind the indentation: it marks the code block."),
 ("Lists and Dictionaries",
  "A list stores ordered data that can be changed; a dict stores key-value pairs. Both are the most frequently used data structures in Python."),
 ("Functions and Modularity",
  "Functions split a program into small parts, each with one job. Use return to give back a result and choose names that explain what the function does. Modular programs are easier to read, test, and extend."),
],
"sql": [
 ("SELECT: Reading Data",
  "SQL (Structured Query Language) is used to manage data in relational databases. SELECT chooses columns from a table; the * sign means all columns."),
 ("WHERE, ORDER BY, LIMIT",
  "WHERE filters rows, ORDER BY sorts results (ASC ascending, DESC descending), and LIMIT restricts how many rows are shown."),
 ("INSERT, UPDATE, DELETE",
  "Three commands change data: INSERT adds rows, UPDATE modifies them, and DELETE removes them. Always include WHERE on UPDATE and DELETE so you do not change the whole table."),
 ("JOIN: Combining Tables",
  "JOIN combines rows from two tables based on related columns, usually a foreign key. INNER JOIN returns only the rows that match in both tables."),
],
"java": [
 ("Java Program Structure",
  "A Java program lives inside a class. Execution starts from the main method. Java is an object-oriented language that is compiled to bytecode and run on the JVM."),
 ("Variables and Data Types",
  "Java is statically typed: a variable's type must be declared. Common primitive types: int, double, boolean, char. String is a class for text."),
 ("Classes and Objects",
  "A class is a blueprint; an object is built from it. A class contains attributes (data) and methods (behavior). The keyword new creates an object."),
 ("Arrays and Loops",
  "An array stores a fixed number of values of the same type. A for or for-each loop is used to walk through it."),
],
"php": [
 ("PHP Basic Syntax",
  "PHP runs on the server and produces HTML. PHP code sits inside <?php ... ?> tags. Each statement ends with a semicolon, and variables start with a $ sign."),
 ("Arrays and Loops",
  "PHP has indexed arrays and associative arrays (key-value). foreach walks through an array concisely."),
 ("Functions",
  "Functions are created with the function keyword. Parameter and return types can be declared to make code clearer and safer."),
 ("Handling Form Data",
  "Form data arrives through the superglobals $_POST or $_GET. Always validate and clean input before using it; use htmlspecialchars() when displaying it again to prevent XSS."),
],
"c": [
 ("Your First C Program",
  "C is a foundational language close to the hardware. A program starts from the main() function. The stdio.h header provides printf and scanf for input and output."),
 ("Variables and Input",
  "C is statically typed: int for whole numbers, float/double for decimals, char for characters. scanf reads input; use %d for int and %f for float. Note the & sign in scanf."),
 ("Loops and Conditionals",
  "for, while, and do-while repeat code; if/else if/else handles branching. The example below prints the even numbers from 1 to 10."),
 ("Arrays and Basic Pointers",
  "An array stores data of the same type. A pointer stores a memory address; the & operator takes an address and * accesses the value at that address. Pointers are the key to understanding memory in C."),
],
"cpp": [
 ("Your First C++ Program",
  "C++ extends C with object-oriented programming and the standard library (STL). cout prints output and cin reads input from the iostream library."),
 ("Vectors and Strings",
  "std::vector is a dynamic array whose size can change, and std::string handles text safely. Both are far more convenient than C-style arrays and char[]."),
 ("Classes and Objects",
  "A class bundles data and behavior. A constructor initializes the object, while private/public modifiers control access to class members."),
 ("STL Algorithms",
  "The algorithm header provides ready-made functions such as sort, find, and count. Using them saves time and reduces bugs compared with rewriting them."),
],
"csharp": [
 ("Your First C# Program",
  "C# is a modern language from Microsoft for .NET, desktop and web apps, and Unity games. Console.WriteLine prints text to the console."),
 ("Variables and Data Types",
  "C# is statically typed but supports var for type inference. Common types: int, double, bool, string. String interpolation uses the $ prefix."),
 ("Lists and LINQ",
  "List<T> is a dynamic collection. LINQ lets you filter and process collections with concise syntax, similar to SQL."),
 ("Classes and Properties",
  "C# classes use properties (get/set) to access data in a controlled way. A constructor prepares the object when it is created."),
],
"react": [
 ("Components",
  "React builds interfaces from components: functions that return JSX (HTML inside JavaScript). Component names must start with a capital letter."),
 ("Props",
  "Props are data passed from a parent component to a child, like HTML attributes. Props are read-only inside the receiving component."),
 ("State with useState",
  "State stores data that changes and triggers a re-render when it does. The useState hook returns the current value and a function to change it."),
 ("Rendering Lists and Conditions",
  "Use map to render lists and give each item a unique key property. Conditional rendering uses the ternary operator or &&."),
],
"mysql": [
 ("Creating Databases and Tables",
  "MySQL is a relational database management system. A database is created with CREATE DATABASE, and the data structure is defined with CREATE TABLE together with each column's type."),
 ("Data Types and Keys",
  "Choose the most suitable data type: INT for whole numbers, VARCHAR(n) for short text, DATE for dates, DECIMAL for precise numbers. A PRIMARY KEY identifies a row uniquely, and a FOREIGN KEY links tables."),
 ("Aggregation with GROUP BY",
  "Aggregate functions (COUNT, SUM, AVG, MIN, MAX) summarize many rows. GROUP BY groups rows, and HAVING filters the groups."),
 ("Indexes and EXPLAIN",
  "An index speeds up searches on frequently filtered columns, at the cost of space and write speed. EXPLAIN shows how MySQL executes a query so you can optimize it."),
],
}

# ---------------------------------------------------------------- quiz: (pertanyaan, [opsi], penjelasan); opsi yang sama dibiarkan
QUIZ_EN = {
"html": [
 ("The abbreviation HTML stands for...", None, "HTML = HyperText Markup Language."),
 ("Which tag is correct for the largest heading?", None, "<h1> is the highest-level heading."),
 ("Which attribute gives alternative text to an image?", None, "alt is read by screen readers and shown when the image fails to load."),
 ("Which element creates a numbered list?", None, "<ol> = ordered list; <ul> is bulleted."),
],
"css": [
 ("CSS is used to...", ["Control page appearance", "Store data", "Create a database", "Run servers"], "CSS controls how HTML elements look."),
 ("Selector for a class named kartu?", None, "A class uses a dot, an id uses #."),
 ("Which property sets the space INSIDE an element's border?", None, "padding = inner space; margin = outer space."),
 ("Which display value gives a flexible layout?", None, "display: flex enables Flexbox."),
],
"javascript": [
 ("Which keyword declares a constant that cannot be reassigned?", None, "const prevents the variable from being reassigned."),
 ("What is the result of typeof \"halo\"?", None, "typeof \"halo\" returns \"string\"."),
 ("Which array method filters elements?", None, "filter returns the elements that satisfy the condition."),
 ("How do you select the element with id=\"judul\"?", None, "querySelector uses CSS selectors; an id starts with #."),
],
"python": [
 ("What is the output of print(2 ** 3)?", None, "** is the power operator: 2 to the power of 3 = 8."),
 ("Which data structure holds key-value pairs?", None, "A dict stores keys and values."),
 ("Which keyword defines a function?", ["func", "def", "function", "lambda only"], "Functions are defined with def."),
 ("What is the result of len([1, 2, 3, 4])?", None, "len counts the elements: 4."),
],
"sql": [
 ("Which command reads data?", None, "SELECT chooses data from a table."),
 ("Which clause filters rows?", ["FILTER", "HAVING only", "WHERE", "ORDER BY"], "WHERE filters rows before they are grouped."),
 ("Sort from largest to smallest?", None, "DESC = descending."),
 ("JOIN is used to...", ["Delete a table", "Combine rows from two tables", "Create an index", "Copy a database"], "JOIN combines tables based on related columns."),
],
"java": [
 ("The entry point of a Java program?", None, "Execution starts from public static void main."),
 ("Which data type is used for text?", ["char[] only", "String", "text", "Str"], "String is a class for text."),
 ("Which keyword creates an object?", None, "new ClassName() creates an object."),
 ("Java runs on...", ["The JVM", "The CLR", "A Python interpreter", "The browser"], "Java bytecode is run by the Java Virtual Machine."),
],
"php": [
 ("A PHP variable starts with...", None, "Example: $nama."),
 ("Which statement displays text?", None, "echo prints output."),
 ("Which superglobal holds POST form data?", None, "$_POST contains POST form data."),
 ("Which function prevents XSS when displaying input?", None, "htmlspecialchars converts special HTML characters."),
],
"c": [
 ("Which function prints to the screen in C?", None, "printf from stdio.h."),
 ("Which printf format is for integers?", None, "%d = int; %f = float; %s = string; %c = char."),
 ("Which operator takes a variable's address?", None, "& takes the address; * accesses the value of a pointer."),
 ("The first index of an array in C?", ["0", "1", "-1", "It depends"], "Array indexes start at 0."),
],
"cpp": [
 ("The standard output object in C++?", None, "cout from <iostream>."),
 ("Dynamic array in the STL?", ["vector", "stack only", "map", "pair"], "std::vector can change its size."),
 ("STL function for sorting?", None, "sort(begin, end) from <algorithm>."),
 ("Which modifier makes a member accessible only inside the class?", None, "private restricts access to inside the class."),
],
"csharp": [
 ("Command to print text to the console?", None, "Console.WriteLine from the System namespace."),
 ("What is var for in C#?", ["Dynamic typing", "Compile-time type inference", "A global variable", "A constant"], "var lets the compiler infer the type; it is still statically typed."),
 ("LINQ is used to...", ["Draw the UI", "Process and filter collections", "Run SQL Server", "Create classes"], "LINQ = Language Integrated Query."),
 ("Syntax for an auto-property?", None, "Example: public string Nama { get; set; }."),
],
"react": [
 ("A React component must start with a ... letter", ["Capital", "Lowercase", "Number", "Underscore"], "A capital letter distinguishes it from a normal HTML tag."),
 ("Which hook stores local state?", None, "useState returns [value, setter]."),
 ("Data passed from parent to child is called...", None, "Props are read-only."),
 ("Which property is required when rendering a list with map?", None, "key helps React track list items."),
],
"mysql": [
 ("Command to create a new table?", None, "CREATE TABLE name (...)."),
 ("Attribute for an auto-increasing value?", None, "AUTO_INCREMENT is commonly used on primary keys."),
 ("Aggregate function to count rows?", None, "COUNT(*) counts rows."),
 ("How do you see a query's execution plan?", None, "EXPLAIN SELECT ... shows the execution plan."),
],
}

# ---------------------------------------------------------------- cheat sheet: deskripsi saja (sejajar dengan content/reference.py)
REF_EN = {
"html": ["Nested headings; h1 is the most important", "Text paragraph", "Link to another page", "Display an image with alternative text",
         "Bulleted / numbered lists and their items", "Table, rows, and cells", "Form and input fields", "Generic block / inline container",
         "Semantic elements that structure a page"],
"css": ["Basic form of a CSS rule", "Text and background color", "Outer space, inner space, border", "One-dimensional flexible layout",
        "Two-dimensional layout (rows and columns)", "Rules for specific screen widths", "Class and id selectors", "Font family and size",
        "Style when the cursor is over an element"],
"javascript": ["Declare constants and variables", "Function declaration", "Arrow function", "Process arrays functionally", "Select a DOM element",
               "Attach an event handler", "Fetch data from the network", "Convert JSON <-> object", "Template literal"],
"python": ["Display a value", "Read text input", "Conditional branching", "Loop n times", "Conditional loop", "list and dict", "Define a function",
           "Frequently used built-in functions", "Handle errors", "Open a file safely"],
"sql": ["Read data", "Filter rows", "Sort results", "Add a row", "Modify rows", "Delete rows", "Combine tables", "Group rows and filter groups", "Aggregate functions"],
"java": ["Program entry point", "Print to the console", "Common data types", "Conditional branching", "For loop", "Define a class", "Create an object",
         "Dynamic list", "Exception handling"],
"php": ["PHP code block", "Variables start with $", "Display output", "Associative array", "Iterate over an array", "Define a function",
        "Form / URL data", "Prevent XSS when displaying input", "Include another file"],
"c": ["Include the I/O library", "Program entry point", "Print with a format", "Read input", "Conditional branching", "Loops", "Fixed-size array",
      "Pointer to the address of x", "Dynamic memory allocation and release"],
"cpp": ["Input/output library", "Print output", "Read input", "Dynamic array", "Text type", "Define a class", "Sort (STL)", "Range-based for",
        "Smart pointer (freed automatically)"],
"csharp": ["Print to the console", "Declaration with type inference", "Common data types", "Conditional branching", "Iterate over a collection", "Dynamic list",
           "Filtering with LINQ", "Class with a property", "Exception handling"],
"react": ["Function component", "Pass props", "Local state", "Side effects after render", "Render a list", "Conditional rendering", "Event handling", "Export a component"],
"mysql": ["Create a database", "Create a table", "Common data types", "Primary key and foreign key", "Auto-increasing value", "Create an index",
          "View a query's execution plan", "View the list of tables and their structure", "Paginate results"],
}

# ---------------------------------------------------------------- katalog bahasa
TAGLINE_EN = {
    "html": "The skeleton and structure of web pages.", "css": "Colors, layout, and the look of pages.", "javascript": "Make web pages interactive.",
    "python": "A versatile language: web, data, AI, automation.", "sql": "The standard language for managing databases.",
    "java": "An object-oriented language for large-scale applications.", "php": "A server-side language for building dynamic sites.",
    "c": "The foundation of systems programming and memory.", "cpp": "C with OOP and a rich standard library.",
    "csharp": "A modern language for .NET, games (Unity), and desktop.", "react": "A component-based UI library built on JavaScript.",
    "mysql": "The most popular relational database system.",
}
DOCS_NAME_EN = {"Dokumentasi Python": "Python Documentation"}

# ---------------------------------------------------------------- modul bawaan: (judul, deskripsi) sejajar dengan SEED_MODULES
SEED_EN = [
    ("Introduction to HTML", "Basic web page structure and main tags."), ("CSS Basics", "Selectors, colors, and simple layout."),
    ("Python Variables and Data Types", "Learn variables, data types, and operators."), ("Python Conditionals and Loops", "if/elif/else, for, and while."),
    ("Python Functions and Modularity", "Splitting a program into structured functions."), ("Interactive JavaScript", "The DOM and events on web pages."),
    ("Basic SQL Queries", "SELECT, WHERE, and ORDER BY."), ("MySQL Database Design", "Normalization and relationships between tables."),
]

# ---------------------------------------------------------------- roadmap: (judul, deskripsi, [catatan langkah]) sejajar dengan ROADMAP
ROADMAP_EN = [
    ("Front-End Developer", "Build interactive and responsive web interfaces.",
     ["Start with page structure.", "Make it beautiful and responsive.", "Add interactivity.", "Build component-based UIs."]),
    ("Back-End Developer", "Create server logic and store data.",
     ["Master programming fundamentals.", "Manage data with queries.", "Build dynamic server-side sites.", "Design efficient databases."]),
    ("Software Engineer", "Understand computer fundamentals and large-scale applications.",
     ["Understand memory and pointers.", "Add OOP and the STL.", "Build object-oriented applications.", "Explore .NET and Unity games."]),
    ("Data and Automation", "Process data and automate work.",
     ["The main language for data and AI.", "Retrieve and summarize data.", "Manage relational databases."]),
]

# ---------------------------------------------------------------- halaman info: (judul, [(judul bagian, isi)]) sejajar dengan INFO
INFO_EN = {
    "tentang": ("About UG-Stack", [
        ("What is UG-Stack?", "UG-Stack is a Python (Flet) programming learning platform that runs on the web and Android. The lessons, cheat sheets, and quizzes are written in-house, then enriched automatically with content from trusted sources."),
        ("Automatic content sources", "Wikipedia (summaries), MDN Web Docs (web references), Stack Overflow (top questions), DEV Community (community articles), and GitHub (popular repositories). Everything is fetched through public APIs, always links back to the original source, and is cached for 24 hours so it still opens offline."),
        ("Content licenses", "Text from Wikipedia, MDN, and Stack Overflow is CC BY-SA licensed and belongs to its original authors. UG-Stack only shows summaries and links, not full copies of articles."),
    ]),
    "komunitas": ("Community and Contact", [
        ("Join in", "Follow UG-Stack updates, ask questions, and share projects with fellow learners. Official community links can be added by the maintainer in content/pages.py."),
        ("Need help?", "Start from the Roadmap or Tutorial page. For specific questions, use the Search feature: it shows related questions from Stack Overflow."),
    ]),
    "aplikasi": ("Install the UG-Stack App", [
        ("Web", "Run python main.py and open http://127.0.0.1:8550 in your browser. The layout adapts automatically to the screen width."),
        ("Android (APK)", "Install the Flutter SDK, JDK 17, and the Android SDK, then run flet build apk in the project folder. Copy the .apk file from build/apk to your phone and install it. Details are in the README."),
        ("Data in the app", "On the APK, user data and the content cache are stored in the device storage so they remain after the app is closed."),
    ]),
    "spaces": ("UG-Stack Spaces", [
        ("A space for code experiments", "Use the Try it Editor to try code examples from each lesson. Open a lesson, then press the Try it Yourself button to load the code into the editor."),
        ("Coming soon", "Saving personal projects and sharing code result links."),
    ]),
}

# ---------------------------------------------------------------- soal tambahan (urutan sejajar dengan content/quizzes.py)
QUIZ_EN["html"].extend([
 ("Which element creates a link?", None, "<a> with the href attribute creates a link."),
 ("Which is the correct closing tag for a paragraph?", None, "Every <p> is closed with </p>."),
 ("Which attribute makes a form field mandatory?", None, "The required attribute makes the browser validate the field."),
 ("Which semantic element marks the main navigation?", None, "<nav> marks a group of navigation links."),
])
QUIZ_EN["css"].extend([
 ("Which property changes text color?", None, "The color property sets text color."),
 ("Which unit is relative to the screen width?", None, "vw = 1% of the viewport width."),
 ("Which flex setting centers items along the main axis?", None, "justify-content controls alignment on the main axis."),
 ("Which selector applies while the cursor is over a button?", None, ":hover applies while the cursor is over an element."),
])
QUIZ_EN["javascript"].extend([
 ("What is the result of 2 + \"2\" in JavaScript?", None, "The + operator concatenates strings, so the result is \"22\"."),
 ("How do you change an element's text?", None, "textContent changes the element's text."),
 ("Which array method adds an element at the end?", None, "push adds an element to the end of the array."),
 ("Which operator compares value and type?", None, "=== compares both value and type."),
])
QUIZ_EN["python"].extend([
 ("How do you write a single-line comment in Python?", None, "Comments start with #."),
 ("What is the result of 7 // 2?", None, "// is floor division: 7 // 2 = 3."),
 ("Which keyword handles errors?", None, "try ... except catches errors."),
 ("Which data type is immutable?", None, "A tuple cannot be changed after it is created."),
])
QUIZ_EN["sql"].extend([
 ("Which aggregate function gives the average?", None, "AVG computes the average."),
 ("Which clause groups rows?", None, "GROUP BY groups rows."),
 ("Which command deletes specific rows?", None, "DELETE FROM ... WHERE removes rows."),
 ("Which key links two tables?", None, "A foreign key references another table's primary key."),
])
QUIZ_EN["java"].extend([
 ("Which data type stores decimal numbers?", None, "double stores decimal numbers."),
 ("Which collection has a dynamic size?", None, "An ArrayList can change its size."),
 ("Which keyword is used for inheritance?", None, "extends creates a subclass."),
 ("Which method runs automatically when an object is created?", ["Destructor", "Constructor", "main", "finalize"], "The constructor initializes a new object."),
])
QUIZ_EN["php"].extend([
 ("Which operator concatenates strings in PHP?", None, "The dot (.) concatenates strings."),
 ("Which function counts array elements?", None, "count() counts array elements."),
 ("Which superglobal holds data from the URL?", None, "$_GET holds URL parameters."),
 ("How do you include another file?", None, "include brings in another PHP file."),
])
QUIZ_EN["c"].extend([
 ("Which type stores a single character?", None, "char stores one character."),
 ("Which function allocates dynamic memory?", None, "malloc allocates memory on the heap."),
 ("What is the result of 10 % 3?", None, "% is the remainder: 10 % 3 = 1."),
 ("What marks the end of a C string?", None, "A string ends with the null character '\\0'."),
])
QUIZ_EN["cpp"].extend([
 ("Which operator creates an object on the heap?", None, "new allocates a dynamic object."),
 ("Which symbol declares a reference (alias) to a variable?", None, "int &r = x; creates a reference (alias)."),
 ("Which container stores key-value pairs?", None, "std::map stores key-value pairs."),
 ("How do you write public inheritance?", None, "Inheritance uses a colon and an access specifier."),
])
QUIZ_EN["csharp"].extend([
 ("How do you create a list of strings?", None, "List<T> is a generic list."),
 ("Which keyword declares a constant?", None, "const declares a constant."),
 ("The ?. operator is used for...", ["Safe null checking", "Loops", "Division", "String comparison"], "The null-conditional operator avoids NullReferenceException."),
 ("Which statement handles exceptions?", None, "try/catch handles exceptions."),
])
QUIZ_EN["react"].extend([
 ("Which hook handles side effects such as loading data?", None, "useEffect runs after render."),
 ("Which JSX syntax displays the variable nama?", None, "Curly braces embed JavaScript expressions."),
 ("How is the CSS class attribute written in JSX?", None, "JSX uses className."),
 ("State should be changed with...", ["The setter function from useState", "Mutating the variable directly", "document.getElementById", "window.state"], "Use the setter so React re-renders."),
])
QUIZ_EN["mysql"].extend([
 ("Which command adds a column to a table?", None, "ALTER TABLE ... ADD COLUMN adds a column."),
 ("Which data type stores a date?", None, "DATE stores a date."),
 ("Which clause limits the number of rows?", None, "LIMIT n limits the number of rows."),
 ("Which function joins text?", None, "CONCAT joins strings."),
])
