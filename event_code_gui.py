import tkinter as tk
from tkinter import Text, Button, filedialog, messagebox
import os
import csv

class TextCategorizerApp:
    def __init__(self, root):
        self.root = root
        self.file_prefix = '' # {subject}_{story}
        self.parent_save_dir = '' # xx/recall_coding
        self.story = '' # name of story
        
        # name GUI
        self.root.title("Transcript Event Coding GUI v1")
        self.root.geometry("2660x1700")
        # add instructions text to top of GUI
        instruction_title = tk.Label(self.root, text="INSTRUCTIONS:")
        instruction_title.pack(pady=5, padx = 5, anchor="w", side="top", fill="x") 
        instruction_label = tk.Label(self.root, text="Click IMPORT on the top right to import recall transcripts. Highlight words or phrases and click a category button to assign to that category.\nCategories are mutually exclusive. To change a categorized word/phrase to another category, highlight the word/phrase and then click the new category.\n\
                                     To remove a category label from a word/phrase, highlight the word/phrase and click \'Clear\'.\nTo denote non-recall content, use curly brackets around relevant words/phrases (e.g. \'{It's an amusing story, all in all.}\').\nWhen finished, click \'Save\' to output csv file with all word/phrases and their corresponding category codes. The input box will then clear and can be used again.", justify="left")
        instruction_label.pack(pady=5, padx = 1, anchor="w", side="top", fill="x") 
        
        # create text box for transcribed recall to be pasted into
        self.text_area = Text(self.root, wrap="word",font=("Lato", 14), height=40, width=85,undo = True)
        self.text_area.pack(padx=10, pady=10, side="left")

        # categories - make sure name's align with colors assigned below in get_category_color
        self.categories_nar = ["Event-NAR", "Place-NAR", "Time-NAR", "Perceptual-NAR", "Emotion/Thought-NAR", "Semantic-NAR"]
        self.categories_par = ["Emotion/Thought-PAR", "Semantic-PAR"]
        self.categories_other=["Repetitions","Other"]
        #self.categories = np.concatenate((self.categories_nar,self.categories_par,self.categories_other))
        
        # create category buttons
        category_frame_nar = tk.Frame(self.root)
        category_frame_nar.pack(side="left", padx=5)
        label_nar = tk.Label(category_frame_nar,text = "Narrator",font='Helvetica 18 bold')
        label_nar.pack(anchor="w", side="top")

        self.category_buttons_nar = []
        for category in self.categories_nar:
            color = self.get_category_color(category)
            btn = Button(category_frame_nar, text=category, command=lambda cat=category: self.assign_category(cat), borderwidth=3, relief="solid", bg=color, highlightbackground=color)
            btn.pack(anchor="w", padx=5)
            self.category_buttons_nar.append(btn)

        category_frame_par = tk.Frame(self.root)
        category_frame_par.pack(side="left", padx=5)
        label_par = tk.Label(category_frame_par,text = "Participant",font='Helvetica 18 bold')
        label_par.pack(anchor="w", side="top")
        self.category_buttons_par = []
        for category in self.categories_par:
            color = self.get_category_color(category)
            btn = Button(category_frame_par, text=category, command=lambda cat=category: self.assign_category(cat), borderwidth=3, relief="solid", bg=color, highlightbackground=color)
            btn.pack(anchor="w", padx=5)
            self.category_buttons_par.append(btn)


        category_frame_other = tk.Frame(self.root)
        category_frame_other.pack(side="left", padx=5)
        label_other = tk.Label(category_frame_other,text = "Other",font='Helvetica 18 bold')
        label_other.pack(anchor="w", side="top")
        self.category_buttons_other = []
        for category in self.categories_other:
            color = self.get_category_color(category)
            btn = Button(category_frame_other, text=category, command=lambda cat=category: self.assign_category(cat), borderwidth=3, relief="solid", bg=color, highlightbackground=color)
            btn.pack(anchor="w", padx=5)
            self.category_buttons_other.append(btn)

        # add button to clear category assignment
        button_frame = tk.Frame(self.root)
        button_frame.pack(side="left", padx=5)
        clear_btn = Button(button_frame, text="Clear", command=self.clear_category)
        clear_btn.pack(side = "left", pady=10)
        
        # add button to save file as csv
        submit_btn = Button(self.root, text="SAVE", command=self.save_to_csv)
        submit_btn.pack(side = "top", padx=1)

        self.category_assignments = {}
        import_btn = Button(self.root, text="IMPORT", command=self.import_file)
        import_btn.pack(side = "top",padx = 1)
        
        #self.marked_indices = []

    # assigns selected word/phrase to category
    def assign_category(self, category):
        selected_indices = self.text_area.tag_ranges(tk.SEL)
        if selected_indices:
            start, end = selected_indices
            selected_text = self.text_area.get(start, end)

            existing_category = self.category_assignments.get(selected_text)
            if existing_category:
                self.text_area.tag_remove(existing_category, start, end)
            # else:
            #     selected_indices_range = list(range(start,end))
            #     intersection = set(self.marked_indices)&set(selected_indices_range)
            #     if intersection:
            #         # todo: 
            #         # stores correspondence between text, category, and marked indices (a list of text and indices as keys)
            #         # search for the intersection in marked indices 
            #         # change indices and marked text in category_assignments 
            #         pass
            self.category_assignments[selected_text] = category
            self.text_area.tag_add(category, start, end)
            self.text_area.tag_config(category, background=self.get_category_color(category))
            #self.marked_indices.extend()

    # clears category from word/phrase so that there is no label
    def clear_category(self):
        selected_indices = self.text_area.tag_ranges(tk.SEL)
        if selected_indices:
            start, end = selected_indices
            selected_text = self.text_area.get(start, end)

            existing_category = self.category_assignments.get(selected_text)
            if existing_category:
                self.text_area.tag_remove(existing_category, start, end)
                del self.category_assignments[selected_text]
            else: 
                messagebox.showerror("Error clearing tag", "An existing tag was not found for the selected text. Make sure you've selected all the text for this tag (including whitespace) and try again. ")

    # Assign unique hex colors for each category; aim to use pretty light colors so you can still read the text when it's highlighted. For more categories, can also add colors to actual text rather than highlighting
    def get_category_color(self, category):
        colors = {"Event-NAR": "#B65FCF", "Place-NAR": "#b7ff87", "Time-NAR": "#bdd2ff", "Perceptual-NAR":"#ffc7f8", "Emotion/Thought-NAR":"#F5B7B1",
                   "Semantic-NAR":'#A3E4D7',"Emotion/Thought-PAR":'#F9E79F', "Semantic-PAR":'#E59866',"Repetitions":'#CCD1D1',"Other":'#95A5A6',"Conditional":"#ffc869"}
        return colors.get(category, "#FFFFFF")  # Default to white if category not found
    
    # save file to csv, with one column for selected text, and one column for corresponding category label
    def save_to_csv(self):
        if self.file_prefix == '':
            filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        else: # file naming: {subject}_{story}_coding.csv
            details_save_dir = os.path.join(self.parent_save_dir,'coded_details')
            if not os.path.exists(details_save_dir):
                os.makedirs(details_save_dir)
            filename = os.path.join(details_save_dir,self.file_prefix+'_coding.csv')

        if filename:
            with open(filename, "w") as file:
                wr = csv.writer(file)
                wr.writerow(['Utterance','Category'])
                #file.write("Utterance,Category\n")
                for word, category in self.category_assignments.items():
                    #file.write(f"{word},{category}\n")
                    wr.writerow([str(word),str(category)])
                
                # after saving out text with categories, iterate through entire text to save each string within curly brackets as a separate entry
                text_content = self.text_area.get("1.0", tk.END)
                nested_texts = self.extract_nested_texts(text_content)
                for nested_text in nested_texts:
                    #file.write(f"{nested_text},non-recall\n")
                    wr.writerow([str(nested_text),'non-recall'])
            file.close()
            messagebox.showinfo("Success", "CSV file saved successfully!")

            # save recall portions only
            clean_recall = self.extract_recall_only(text_content)
            clean_recall_save_dir = os.path.join(self.parent_save_dir,'clean_recall')
            if not os.path.exists(clean_recall_save_dir):
                os.makedirs(clean_recall_save_dir)
            clean_recall_filename = self.file_prefix+'_recall_only.txt'
            with open(os.path.join(clean_recall_save_dir,clean_recall_filename),'w') as f:
                f.write(clean_recall)
            messagebox.showinfo("Success", "Clean recall saved successfully!")
            # clears text box for next transcript so that GUI can stay open/doesn't have to be re-loaded for each transcript
            self.clear_text_area()

    def extract_nested_texts(self, text):
        nested_texts = []
        start_index = text.find('{')
        while start_index != -1:
            end_index = text.find('}', start_index)
            if end_index != -1:
                nested_texts.append(text[start_index + 1:end_index].strip())
                start_index = text.find('{', end_index + 1)
            else:
                break
        return nested_texts
    
    def extract_recall_only(self,text):
        recall = ''
        end_index = -1
        start_index = text.find('{')
        while start_index != -1:
            recall+=text[end_index+1:start_index]
            end_index = text.find('}', start_index)
            start_index = text.find('{', end_index + 1)
        recall+=text[end_index+1:]
        recall = ' '.join(recall.split()) # get rid of extra whitespace
        return recall
    
    def clear_text_area(self):
        self.text_area.delete("1.0", tk.END)
        self.category_assignments = {}
        self.file_prefix = ''
        self.parent_save_dir = ''
        self.story = ''

    def import_file(self):
        filename = filedialog.askopenfilename()
        story_recall_dir = os.path.split(filename)[0] # xx/recall_transcript/story
        self.file_prefix = os.path.split(filename)[-1].split('.')[0] # {subject}_{story}
        self.story = os.path.split(story_recall_dir)[-1] # story
        parent_dir = os.path.split(os.path.split(story_recall_dir)[0])[0] # xx/
        self.parent_save_dir = os.path.join(parent_dir,'recall_coding',self.story) # xx/recall_coding/story
        with open(filename,'r') as f:
            transcript = f.read()
        self.text_area.insert(tk.END, transcript)


if __name__ == "__main__":
    root = tk.Tk()
    app = TextCategorizerApp(root)
    root.mainloop()
