import genanki
import json
import os
import fitz 




try:

    for file in os.listdir(os.getcwd()):
        if file.endswith(".pdf"):
            pdf_path = file
           

    pdf = fitz.open(pdf_path)
    zoom_faktor = 150 / 72.0
    mat = fitz.Matrix(zoom_faktor, zoom_faktor)

    for page_num in range(len(pdf)):
        page = pdf.load_page(page_num)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        output_datei = f"slides/slide_{page_num + 1}.png"
        pix.save(output_datei)

    pdf.close()
except Exception as e:
    print(f"Fehler beim Verarbeiten der PDF: {e}")


# JSON laden
with open("karten.json", "r", encoding="utf-8") as f:
    data = json.load(f)

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
        f"{pdf_path[:-4]}"
    )

    for card in data:
        note = genanki.Note(
            model=model,
            fields=[card["frage"], card["antwort"]]
        )
        deck.add_note(note)

    

    media_files = [f"slides/slide_{i}.png" for i in range(1, len(os.listdir("slides")) + 1)]
    print(media_files)

    genanki.Package(deck, media_files=media_files).write_to_file(f"{pdf_path[:-4]}.apkg")