from flask import url_for, render_template, redirect, make_response
from math import factorial

from flask.ext.wtf import Form, BooleanField, IntegerField
from flask.ext.wtf import Required, FieldList,  SelectField

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def C(X,Y):
    if X < 0 or Y < 0 or X - Y < 0:
        return 0
    return factorial(X) / float(factorial(Y) * factorial(X-Y));

class ResourceForm(Form):
    decksize = IntegerField('decksize', validators = [Required()], default = 60)
    resourcesInDeck = IntegerField('resourcesInDeck', validators = [Required()], default = 24)
    turns = IntegerField('turns', validators = [Required()], default = 30)
    turn_one_draw = IntegerField('turn_one_draw', validators = [Required()], default = 7)
    resource_types = FieldList(IntegerField("resource_types",validators = [Required()]), min_entries=0, max_entries=5)
    resource_types_names = FieldList(SelectField("resource_types_names",validators = [Required()], choices = [('Blood','Blood'), ('Diamond','Diamond'), ('Ruby','Ruby'), ('Sapphire','Sapphire'), ('Wild', 'Wild')]), min_entries=0, max_entries=5)
    accumulate = BooleanField('accumulate')
    elim_unplayable = BooleanField('elim_unplayable')
    
    def validate_on_submit(self):
        superVal = super(ResourceForm, self).validate_on_submit()
        customVal = True
        
        if self.resourcesInDeck.data < 0:
            self.resourcesInDeck.errors.append('This field is required.')
            customVal = False
        if self.decksize.data < 0:
            self.decksize.errors.append('This field is required.')
            customVal = False
        if self.turns.data < 0:
            self.turns.errors.append('This field is required.')
            customVal = False
        if self.turn_one_draw.data < 0:
            self.turn_one_draw.errors.append('This field is required.')
        
        if self.decksize.data < self.resourcesInDeck.data:
            self.decksize.errors.append('Deck Size Must be Larger Than Resources.')
            customVal = False
        if (self.turns.data + self.turn_one_draw.data) > self.decksize.data:
            self.turns.errors.append('Too Many Turns.')
            customVal = False

        return superVal and customVal

class ResourceCalculator():
    @staticmethod
    def accumulateData(data):
        for x in range(0, len(data)):
                for y in range(0,len(data[x])):
                        x_i = len(data)-x-1
                        if x_i > 1:
                            data[x_i-1][y] = data[x_i][y] + data[x_i-1][y]
        return data
    
    @staticmethod
    def resourceTable(decksize, resources, turns, turn_one_draw, types, accumulate, elim_unplayable):
        tableheader = ['Turn']
        tabledata = []
        allprobs = []
        lastempty = 0
        
        for res in range(0,resources+1):
            tableheader.append(res);
        
        for turn in range(turn_one_draw,turns+turn_one_draw):
            ind = 0
            data = []
            
            d = ['%s' % (turn-turn_one_draw+1)]
            for single_type in types:
                d.append(single_type['name'])
            
            data.append(d)
            
            for res in range(0,resources+1):
                ind = ind + 1
                #chances of having at least res on turn turn
                #===============================================================================
                # http://www.kibble.net/magic/magic10.php
                # H (n) = C (X, n) * C (Y - X, Z - n) / C (Y, Z)
                # 
                # X stands for the number of a certain card that you have in the deck.
                # 
                # Y is the number of cards in the deck.
                # 
                # Z is the number of cards you are drawing.
                # 
                # N is the number you are checking for.
                #===============================================================================
                
                if (turn-res) < 0:
                    H = 0
                else:
                    H = C(resources, res)*C((decksize - resources), (turn-res))/float(C(decksize,turn))
                
                d = [float(H*100)]
                
                if ('%.1f%%' % float(H*100)) != '0.0%':
                    lastempty = ind;
                
                for single_type in types:
                    if (turn-res) < 0:
                        H = 0
                    else:
                        H = C(single_type['num'], res)*C((decksize - single_type['num']), (turn-res))/float(C(decksize,turn))
                        
                    d.append(float(H*100))
                    
                data.append(d)
                
                allprobs.append(float(H*100))
            
            if accumulate:
                data = ResourceCalculator.accumulateData(data)
            
            tabledata.append(data)
        
        ret = {'header': tableheader,
               'data': tabledata,
               'max': int(100/(max(allprobs))),
               'lastempty': lastempty,
               }
        return ret
    
    @staticmethod
    def urlFromResourceLink(string, snippets):
        
        form = ResourceForm()
        data = []
        for x in range(0, len(string)):
            if string[x].isalpha():
                string_int = ''
                for y in range(x+1, len(string)):
                    if RepresentsInt(string[y]): 
                        string_int = '%s%s' % (string_int, string[y])
                    else:
                        break
                str_tuple = (string[x],int(string_int))
                data.append(str_tuple)
        types = []
        types_ind = 0
        for item in data:
            if item[0] == 'd':
                form.decksize.data = item[1]
            elif item[0] == 'x':
                form.resourcesInDeck.data = item[1]
            elif item[0] == 'w':
                form.resource_types_names.append_entry()
                form.resource_types.append_entry()
                
                form.resource_types_names[types_ind].data = 'Wild'
                form.resource_types[types_ind].data = item[1]
                
                types_ind = types_ind + 1
            elif item[0] == 'b':
                form.resource_types_names.append_entry()
                form.resource_types.append_entry()
                
                form.resource_types_names[types_ind].data = 'Blood'
                form.resource_types[types_ind].data = item[1]
                
                types_ind = types_ind + 1
            elif item[0] == 'r':
                form.resource_types_names.append_entry()
                form.resource_types.append_entry()
                
                form.resource_types_names[types_ind].data = 'Ruby'
                form.resource_types[types_ind].data = item[1]
                
                types_ind = types_ind + 1
                
            elif item[0] == 'i':
                form.resource_types_names.append_entry()
                form.resource_types.append_entry()
                
                form.resource_types_names[types_ind].data = 'Diamond'
                form.resource_types[types_ind].data = item[1]
                
                types_ind = types_ind + 1
            elif item[0] == 's':
                form.resource_types_names.append_entry()
                form.resource_types.append_entry()
                
                form.resource_types_names[types_ind].data = 'Sapphire'
                form.resource_types[types_ind].data = item[1]
                
                types_ind = types_ind + 1
            elif item[0] == 't':
                form.turns.data = item[1]
            elif item[0] == 'f':
                form.turn_one_draw.data = item[1]
            elif item[0] == 'a':
                if item[1] == 1:
                    form.accumulate.data = True 
                else:
                    form.accumulate.data = False
            elif item[0] == 'e':
                if item[1] == 1:
                    form.elim_unplayable.data = True 
                else:
                    form.elim_unplayable.data = False

        for x in range(0,len(form.resource_types)):
            types.append({'name': form.resource_types_names[x].data,
                          'num': form.resource_types[x].data,
                          })
            print form.resource_types_names[x].data
            print form.resource_types[x].data

        try:
            table = ResourceCalculator.resourceTable(
                                                     form.decksize.data, 
                                                     form.resourcesInDeck.data, 
                                                     form.turns.data, 
                                                     form.turn_one_draw.data, 
                                                     types, 
                                                     form.accumulate.data,
                                                     form.elim_unplayable.data
                                                     )
        except:
            return redirect(url_for('ToolsView:resourceDraw'))
        
        resp = make_response(render_template('tools/resource_draw.html', snippets=snippets, form = form, table=table, hide=1, link = ResourceCalculator.resourceLinkfromForm(form)))
        resp.headers['Cache-Control'] = 'max-age=432000, public'
        return resp;

    @staticmethod
    def resourceLinkfromForm(frm):
        import copy
        form = copy.deepcopy(frm)
        if form.accumulate.data:
            acc = 1
        else:
            acc = 0
        
        if form.elim_unplayable.data:
            elim = 1
        else:
            elim = 0
        
        string = 'd%sx%st%sf%sa%se%s' % (form.decksize.data,form.resourcesInDeck.data,form.turns.data,form.turn_one_draw.data,acc,elim)
        
        x = 0
        for name in form.resource_types_names.entries:
            if name.data == 'Wild':
                val = form.resource_types.entries[x].data
                string = ('%sw%s' % (string,val))
            elif name.data == 'Blood':
                val = form.resource_types.entries[x].data
                string = ('%sb%s' % (string,val))
            elif name.data == 'Ruby':
                val = form.resource_types.entries[x].data
                string = ('%sr%s' % (string,val))
            elif name.data == 'Sapphire':
                val = form.resource_types.entries[x].data
                string = ('%ss%s' % (string,val))
            elif name.data == 'Diamond':
                val = form.resource_types.entries[x].data
                string = ('%si%s' % (string,val))
            x = x+1
        
        return string        
