# Enlisted ESP (Educational Example)

**WARNING:** This project is for educational purposes only. Using this in a live game may violate the game's Terms of Service and result in a ban. This is a highly simplified example and does NOT include any actual EAC bypass mechanisms. Implementing a real bypass is extremely complex and beyond the scope of this example.

## Description

This is a basic ESP (Extra Sensory Perception) program for the game Enlisted. It is a simplified example and does not include any actual EAC bypass mechanisms.  It's intended to demonstrate the basic principles of memory reading and drawing information on the screen.

**Important:** This project requires significant reverse engineering of the Enlisted game to identify the memory locations of the enemy list and their properties.

## Setup

1.  **Install a C++ compiler:** You will need a C++ compiler such as Visual Studio or MinGW.
2.  **Create a new C++ project:** Create a new C++ project in your IDE.
3.  **Add the `src/main.cpp` file to your project.**
4.  **Find the Game Base Address:**  This is the most challenging part.  You will need to use a debugger (like Cheat Engine or x64dbg) to find the base address of the Enlisted game process in memory.  This address will change each time the game is launched.
5.  **Reverse Engineer the Game:**  You will need to reverse engineer the game's memory structures to find the location of the enemy list, and the properties of each enemy (x, y, z coordinates, visibility).
6.  **Replace Placeholders:**  Replace the placeholder values in `src/main.cpp` with the actual game base address and the offsets to the enemy list and their properties.
7.  **Implement Drawing:**  The `DrawESP` function currently only prints to the console.  You will need to implement actual drawing using a graphics API such as DirectX or OpenGL.  This is a complex task and requires significant programming knowledge.
8.  **Compile and Run:** Compile the project and run the executable.

## Disclaimer

This project is for educational purposes only. The author is not responsible for any bans or other consequences that may result from using this program in a live game.

**EAC Bypass:** This project does NOT include any EAC bypass mechanisms. Implementing a real bypass is extremely complex and beyond the scope of this example.  Attempting to bypass EAC may result in a permanent ban from the game.