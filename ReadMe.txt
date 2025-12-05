How to Create a Language Extension Pack
====================

1. Obtain Game Text
① On the game's main interface, click "Settings", then navigate to "Gameplay — Select Language" and click "Create translation". This will automatically open the [language] folder.
② Inside the folder, you will find a file named #GF_default.csv. #GF_default contains the game text in the local language.

2. Translate the Text
① It is recommended to open the CSV file directly with Visual Studio Code and install the Edit CSV plugin for easier editing.
② In the game file, the code format is: "key", "English Text", "Local Language Text".
"key" is a unique identifier. To ensure the game functions properly, do not modify it.
"English Text" is the source text for reference. Do not modify it.
"Local Language Text" is the actual displayed text. You may translate or modify this as needed.
③Future Updates
The file content is mainly divided into two sections: "NormalText" and "SpecialText" (which can be directly searched). If new text is added in future game updates, players can copy the new text based on the "key" into their previous expansion packs and continue creating.

3. Use the Extension Pack
① Ensure the file format remains CSV.
② The file name must follow the format: "#GF_XXX"
"#GF_" is a fixed identifier and must not be changed.
"XXX" can be any text of any length.
③ The file must be placed in the "language" folder.
After meeting the above three conditions, restart the game. Go to "Settings — Language Extension Pack" and select the desired translation to use.