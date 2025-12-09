from flask import Flask, render_template, request
import genanki
import json
import os
import fitz 
import webbrowser

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')    

@app.route('/generate_deck', methods=['POST'])
def generate_deck():

    pdf_file = request.files.get('pdf') 
    filename = pdf_file.filename

    if not filename.endswith('.pdf'):
        return "Bitte eine PDF-Datei hochladen", 400
    
    
    pdf_file.save(filename)

    try:
        json_data = json.loads(request.form.get('json'))

    except Exception as e:
        return f"Falsches Format bei der Gemini-Antwort", 400

    try:

        pdf_file = fitz.open(filename)
        zoom_faktor = 150 / 72.0
        mat = fitz.Matrix(zoom_faktor, zoom_faktor)

        for page_num in range(len(pdf_file)):
            page = pdf_file.load_page(page_num)
            pix = page.get_pixmap(matrix=mat, alpha=False)
            output_datei = f"slides/slide_{page_num + 1}.png"
            pix.save(output_datei)

        pdf_file.close()
        os.remove(filename)
        
    except Exception as e:
        print(e)
        return f"Fehler beim Verarbeiten der PDF", 500

    model = genanki.Model(
        1607392319,
        'Simple Model',
        fields=[
            {'name': 'Frage'},
            {'name': 'Antwort'}
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Frage}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{Antwort}}',
            },
        ])

    deck = genanki.Deck(
        2059400110,
        f"{filename[:-4]}"

    )

    for card in json_data:
        note = genanki.Note(
            model=model,
            fields=[card["frage"], card["antwort"]]
        )
        deck.add_note(note)

    

    media_files = [f"slides/slide_{i}.png" for i in range(1, len(os.listdir("slides")) + 1)]

    
    

    genanki.Package(deck, media_files=media_files).write_to_file(f"{filename[:-4]}.apkg")
    
    return "", 200

if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:5000/")
    app.run(host='0.0.0.0')
    