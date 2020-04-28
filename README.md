# Lowe's hackathon

**Problem Statment**: Build a solution to help the customers find products in the store and help them navigate to the corresponding aisle/shelf. If there is a shopping list, provide the best shopping trip to complete the purchases.


## Proposed Solution

The solution is based on a modified A star path finding algorithm to find the best possible path to collect all the necessary items one needs to buy. Currently the order of the item to be bought is solely based on the distance from the users current position.

### Setting up of the problem

The program is demoed using a custom map constructed reffering to Lowe's shop plan, for the customer to interact with.

![Store Plan for testing the program](https://github.com/Fathaah/Lowe-Path-Finding/blob/master/Map4.jpg)

There is also another map the path finding algorithm uses to avoid obstacles and navigate.

![Obstacle Map](https://github.com/Fathaah/Lowe-Path-Finding/blob/master/p_map3.jpg)

An advantage of such an approach is the scalability of the solution, since Lowe is having more than 2000 stores such an approach minimizes the need of further fine tuning the program for each store. If there is a floor plan and a map as shown above, the application can be easily scaled.

A list of items and its position was arbitrarily choosen to set up a testing environment for the program, these items along with the positional info can be found in *data.csv*.

### Installation

The essential required packages needed to run the solution are:

```
Kivy==1.11.1
Pillow==7.1.1
opencv-python==4.2.0.34
numpy==1.18.2
```

The above installations will automatically install the necessary dependancies.

To execute and run the code, use the following command:

```
python main.py
```

### Working

The starting screen of the application is shown below:

![Starting Screen](https://github.com/Fathaah/Lowe-Path-Finding/blob/master/images/1.PNG)

There is a search bar, then a shopping list button to see the items currently on the list.


![Shopping List](https://github.com/Fathaah/Lowe-Path-Finding/blob/master/images/3.PNG)

Once the Searchbar is clicked a dropdown menu appears with various choices of items the customer can buy or type in the item they need.


![DropDown](https://github.com/Fathaah/Lowe-Path-Finding/blob/master/images/2.PNG)


Once the item/items are selected the algorithm devices a plaussible route through the shop to pick the items up. Below are few examples of the routes generated.
![Example Path](https://github.com/Fathaah/Lowe-Path-Finding/blob/master/images/4.PNG)
![Example Path](https://github.com/Fathaah/Lowe-Path-Finding/blob/master/images/5.PNG)
![Example Path](https://github.com/Fathaah/Lowe-Path-Finding/blob/master/images/6.PNG)

In certain conditions the A star alorithm gets trapped, this happens only when the direction towards the item or object is blocked by an obstacle when it is in the open, meaning outside shelves. This is easily solved by letting the program explore more possible routes, this increases the time for finding the path.

![Example Path](https://github.com/Fathaah/Lowe-Path-Finding/blob/master/images/e.PNG)


ADDED:

Pop up messages for interactive communication with the customer:


![Example Path](https://github.com/Fathaah/Lowe-Path-Finding/blob/master/images/7.PNG)


## Known issues

* The algorithm fails at certain conditions when the item is directly opposite to the hexagon in the case given. Selecting Soil first will demonstrate this issue. This is easily solved by letting the program explore more possible routes, this increases the time for finding the path.

* There is small issues with the positioning of items making the route a bit chaotic. 

## To Do

- [x] Build from scratch, make it more robust and workable structured code.
- [x] Add a shopping list, where use can see items he is willing to buy.
- [x] Allow the customer to remove an item from the shopping list.
- [x] Security Loop
- [x] Create new and modified better map.
- [x] Messages on map like suggestions and detours. 
- [x] Heavy items are to planned to be picked up later on.
- [ ] Customer localization.
- [ ] Reduce the frequency of change in direction, keep the paths straight.
- [ ] Suggestions on what the customer might need, like if he buys screws it's very likely he might need a screwdriver.
- [ ] Improve UI, an applications success hugely depends on the interface.

## NOTES

Currently the customer localization is implemented in the previous version of the code, through barcode scanning of any nearby items or barcodes specifically designed for localizing the customer in the store. A possibility of a vision based system is being studied, using cues deligently palced in the stores to detect customers current location.


