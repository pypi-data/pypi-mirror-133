import json

class n():  # every file
    """For every file `UNCODED`"""
    def entry(file):
        """opens file and return content inside that file"""
        with open(file, "r") as f:
            return file.read()

    def exit(file, writeble):
        """writes inside this file your content"""
        with open(file, "w") as f:
            file.write(writeble)


class j():  # json files
    """For json file"""
    def entry(file):
        """opens json file and return content inside json file"""
        with open(file, "r", encoding="utf-8") as f:
            return file.load(f)
    
    def exit(file, writeble):
        """writes inside json file your content"""
        with open(file, "w",encoding='utf-8') as f:
            json.dump(f, writeble, indent=2,  ensure_ascii=False)


class h():  # html file
    """for html file"""
    def exit(name, title="document", heard=None, body="that body", lang="en"):
        """creates content html file:
            `name`  it's name html file;
            `title` it's title in html file, you can don't write this
            `heard` it's if you want add element in heard
            `body`  it's main setting for wrote html, it write  in `<body> </body>`
            `lang`  it's setting write language for encoding"""
        with open(name+".html", "w") as f:
            content = f"""<!DOCTYPE html>

    <html lang={lang}>

    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
    </head>

    <body>

        {body}
    
    </body>

    </html>
    """
            f.write(content)

    def retext(text):
        letter = ''
        arr = []
        list_ = []
        temp = []
        for i in text.split():
            arr.append(i)
        for i in arr:
            if i == '$':
                list_.append(temp)
                temp = []
            else:
                temp.append(i)
                
        for i in list_:
            content = ''
            for k in range(1, len(i)):
                content += i[k] + ' '
            if i[0] == "$d":
                letter += f'<div> {content} </div> \n\t'
            else:
                cc = i[0].replace("$", '')
                letter += f'<{cc}> {content} </{cc}>'   

        return letter
