# List of available themes for Ace Editor
ace_themes = [
    'chrome', 'clouds', 'crimson_editor', 'dawn', 'dreamweaver',
    'eclipse', 'github', 'iplastic', 'solarized_light', 'textmate',
    'tomorrow', 'xcode', 'kuroir', 'katzenmilch', 'sqlserver',
    'ambiance', 'chaos', 'clouds_midnight', 'cobalt', 'gruvbox',
    'idle_fingers', 'kr_theme', 'merbivore', 'merbivore_soft',
    'mono_industrial', 'monokai', 'pastel_on_dark', 'solarized_dark',
    'terminal', 'tomorrow_night', 'tomorrow_night_blue',
    'tomorrow_night_bright', 'tomorrow_night_eighties', 'twilight',
    'dracula', 'gob', 'vibrant_ink'
]

# List of programming languages supported by Ace Editor
# ace_languages = [
#     'python', 'c_cpp', 'java', 'javascript', 'ruby', 'rust', 'go',
#     'csharp', 'kotlin', 'swift', 'php', 'perl', 'r', 'typescript',
#     'sql', 'html', 'css', 'markdown', 'json', 'xml', 'yaml', 'sh'
# ]

ace_languages = [
    'python', 'c_cpp'
]

# Mapping from Ace Editor language names to execution function languages
execution_languages = {
    'python': 'python',
    'c_cpp': 'c_cpp',
    'java': 'java',
    'javascript': 'javascript',
    # Add other mappings as needed
}

# Default code snippets for each language
default_code_snippets = {
    'python': "print('Hello, Streamlit!')",
    'c_cpp': """#include <iostream>

int main() {
    std::cout << "Hello, C++!" << std::endl;
    return 0;
}
""",
    'java': """public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, Java!");
    }
}
""",
    'javascript': "console.log('Hello, JavaScript!');",
    'ruby': "puts 'Hello, Ruby!'",
    'go': """package main

import "fmt"

func main() {
    fmt.Println("Hello, Go!")
}
""",
    # Add default code for other languages as needed
}

# List of available keybindings for Ace Editor
ace_keybindings = ['vscode', 'ace', 'vim', 'emacs', 'sublime']