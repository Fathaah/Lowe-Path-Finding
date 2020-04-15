

class DataHandler():
    def __init__(self, map, popup):
        self.shopping_list = []
        self.items_dict = {'entrance': [(60,30), 0, (-1,-1), (-1,-1)],'check_out':[(23,4), 0, (23,4), (23,4)],
         'hammer' : [(20, 50), 0, (20, 50), (20, 50)], 'paint': [(29,10),0,(29,0), (29,25) ], 
         'wood' : [(8, 40), 0, (8,36), (8,47)], 'nails': [(47,10),0,(47,0), (47,25)], 'saw': [(12,28), 0, (20, 28), (1, 28)]}
        self.path_finder = PathFinder(dims)
        self.path = []
        self.map = map
        self.popup = popup

    def list_updated(self):
        #print('path')
        self.path, idx, idx_name = self.path_finder.find(self.shopping_list)
        #print(self.path)
        self.map.draw(self.path, idx, idx_name)
        self.popup.updateList(self)
    def add_element(self, element):
        temp = Data(element[0],element[1], element[2], element[3], element[4])
        self.shopping_list.append(temp)
        #print('Appending Successfull')
        #for e in self.shopping_list:
            #print('in shopping list ' + e.item_name)
        self.list_updated()
    def remove_element(self, element, btn):
        print(element[3:])
        temp = self.shopping_list.copy()
        self.shopping_list = []
        for ele in temp:
            if ele.item_name != element[3:]:
                self.shopping_list.append(ele)
        self.list_updated()

            

class Data():
    def __init__(self, name, pos,on_stock, pos_1, pos_2):
        self.item_name = name
        self.pos = pos
        self.on_stock = on_stock
        self.pos_1 = pos_1
        self.pos_2 = pos_2