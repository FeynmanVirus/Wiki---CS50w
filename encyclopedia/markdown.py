import re

def markdownify(title):
    # opening file 
    with open(f"entries/{title}.md") as file:
        # reading into the file
        reading_file = file.read()
        # converting markdown heading to html heading
        for i in range(6, 0, -1):
            reading_file = re.sub(fr"{'#' * i}(.*)", fr"<h{i}>\1</h{i}>", reading_file)
            
        # converting markdown boldface text into html boldface text
        reading_file = re.sub(r'\*\*(.*?)\*\*', r"<b>\1</b>", reading_file)

        # converting markdown italic into html italic text
        reading_file = re.sub(r'_(.*?)_', r"<i>\1</i>", reading_file)
        reading_file = re.sub(r'\*(.*?)\*', r"<i>\1</i>", reading_file)  

        # converting markdown unordered lists into html unordered lis  
        reading_file = re.sub(r'[-+*]\s+(.*)', r'<li>\1</li>', reading_file, flags=re.MULTILINE)
        
        reading_file = re.sub(r'(<li>.*</li>)', fr'<ul>\1', reading_file, 1) 
        reading_file = re.sub(r'(<li>.*</li>)$', fr'\1</ul>', reading_file)  

        # converting markdown links into html links
        reading_file = re.sub(r'\[(.*)\]\(/wiki/(.*)\)', r'''<a href="{% url 'goto' \2 %}">\1</a>''', reading_file)
        
        print(reading_file)
        return reading_file 