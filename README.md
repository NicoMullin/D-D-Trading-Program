![D&D Trading Program Banner](ProgramBanner.png)

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-WIP-orange)


# D&D Trading Program

## Description
The **D&D Trading Program** is a Python-based trading utility designed to enhance the gameplay of Dungeons & Dragons campaigns. This program allows players to simulate dynamic trade systems with fluctuating prices, adjustable modifiers, and customizable items and islands.

This script and program is a work in progress. It is my first script, so there will be bugs at times. Currently, the basis of this program is for my DnD Pirate campaign that I run. Although it says that this is a D&D trading program, it can be used for any system that you like that uses some kind of money. In the final version (whenever that is), I hope it will be cleaner and display more as a TTRPG trading program.

Whether you’re a Dungeon Master looking to add depth to your world or a player managing a trading business, this program provides all the tools to create an engaging trading experience.

## Features
- **Customizable Islands**: Define unique islands with specific items and prices.
- **Dynamic Price Fluctuations**: Simulate real-world trading with randomized price adjustments.
- **Global and Local Modifiers**: Adjust global and item-specific modifiers to create varied trading scenarios.
- **User-Friendly Interface**: Built using `Tkinter`, the GUI is intuitive and easy to use.
- **Save and Load Configurations**: Save your custom settings and reload them anytime.

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.7 or higher
- Required libraries: `tkinter`, `json`

### Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/NicoMullin/D-D-Trading-Program.git
   ```
2. Navigate to the project directory:
   ```bash
   cd D-D-Trading-Program
   ```
3. Run the program:
   ```bash
   python DnD_Trading_Program.py
   ```

## Usage
1. **Start the Program**: Launch the application by running the Python script.
2. **Select an Island**: Choose an island from the dropdown menu to begin trading.
3. **Add Items**: Define the items and their modifiers for trading.
4. **Adjust Modifiers**: Use global and item-specific modifiers to influence prices.
5. **Calculate Prices**: Click the `Calculate Prices` button to view adjusted trading values.
6. **Save Configurations**: Use the save functionality to store your settings for later.

### Screenshots
This is the Main Screen of the program.

![Main Screen](resources/Program1.png)

This is the Create New Island screen when the button is pressed.

![Create New Isalnd](resources/Program2.png)

This is the Add Custom Item screen when the button is pressed.

![Add Custom Item](resources/Program3.png)

This is one item with no modifers. The base price of rice is 100. The program will fluctuate the base item of that item. The Global Modifier is to raise or lower the base price depending on how the island is doing in terms of money. The sell and buy modifiers are for fine tuneing select items.

![Prices!](resources/Program5.png)

The Quantity box overides all other prices. If at None, place will not sell, but will buy at a high price. If at low, sell prices are higher, and buy prices. If at normal there is no modifiers. If at High, the sell prices are dirt cheep but will not buy any of that item

![Quantity](resources/Program6.PNG)



## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with detailed descriptions of your changes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Created by **Nico Mullin**.
- Special thanks to ChatGPT for assistance with the development process.
- Inspired by the intricate trade systems of D&D campaigns.

## Contact
Feel free to reach out for suggestions or questions:
- **GitHub**: [NicoMullin](https://github.com/NicoMullin)



