import asyncio
import os
import codecs
import requests
from modules.scrapper import create_scrapper, Scrapper
from rich import print as rprint
import datetime

SUBJECTS = {
    "aleman": "Alemán",
    "anatomia": "Anatomía Aplicada",
    "analisis-musical": "Análisis Musical",
    "artes-escenicas": "Artes Escénicas",
    "biologia": "Biología",
    "ciencias-de-la-tierra": "Ciencias de la Tierra y Medioambientales",
    "cultura-audiovisual": "Cultura audiovisual",
    "dibujo-artistico": "Dibujo Artístico",
    "dibujo-tecnico": "Dibujo Técnico II",
    "diseno": "Diseño",
    "economia": "Economía de la Empresa",
    "electrotecnia": "Electrotecnia",
    "frances": "Francés",
    "arte": "Fundamentos del Arte",
    "fisica": "Física",
    "geografia": "Geografía",
    "geologia": "Geología",
    "griego": "Griego",
    "historia": "Historia de España",
    "filosofia": "Historia de la Filosofía",
    "historia-de-la-musica": "Historia de la Música y de la Danza",
    "historia-del-arte": "Historia del Arte",
    "imagen": "Imagen",
    "ingles": "Inglés",
    "italiano": "Italiano",
    "latin": "Latín II",
    "lengua-y-literatura": "Lengua Castellana y Literatura",
    "lengua-catalana": "Lengua Catalana y Literatura",
    "lengua-gallego": "Lengua Gallega y Literatura",
    "lengua-vasca": "Lengua Vasca y Literatura",
    "lengua-valenciano": "Lengua y Literatura (Valenciano)",
    "lenguaje-musical": "Lenguaje y Práctica Musical",
    "literatura-castellana": "Literatura Castellana",
    "literatura-catalana": "Literatura Catalana",
    "literatura-universal": "Literatura Universal",
    "matematicas-aplicadas": "Matemáticas Aplicadas a las Ciencias Sociales",
    "matematicas": "Matemáticas II",
    "mecanica": "Mecánica",
    "portugues": "Portugués",
    "quimica": "Química",
    "tecnologia-industrial": "Tecnología Industrial",
    "expresion-plastica": "Técnicas de Expresión Gráfico Plástica"
}

SIMPLE_SUBJECTS = {
    "ALE": "aleman",
    "ANA": "anatomia",
    "ANM": "analisis-musical",
    "ARE": "artes-escenicas",
    "BIO": "biologia",
    "CTM": "ciencias-de-la-tierra",
    "CAV": "cultura-audiovisual",
    "DAR": "dibujo-artistico",
    "DT2": "dibujo-tecnico",
    "DIS": "diseno",
    "ECO": "economia",
    "ELT": "electrotecnia",
    "FRA": "frances",
    "ART": "arte",
    "FIS": "fisica",
    "GEOG": "geografia",
    "GEOL": "geologia",
    "GRI": "griego",
    "HES": "historia",
    "HFI": "filosofia",
    "HMD": "historia-de-la-musica",
    "HAR": "historia-del-arte",
    "IMA": "imagen",
    "ING": "ingles",
    "ITA": "italiano",
    "LAT": "latin",
    "LCL": "lengua-y-literatura",
    "LCV": "lengua-catalana",
    "LGA": "lengua-gallego",
    "LVA": "lengua-vasca",
    "LVL": "lengua-valenciano",
    "LEM": "lenguaje-musical",
    "LIC": "literatura-castellana",
    "LCA": "literatura-catalana",
    "LUN": "literatura-universal",
    "MAC": "matematicas-aplicadas",
    "MAT": "matematicas",
    "MEC": "mecanica",
    "POR": "portugues",
    "QUI": "quimica",
    "TIN": "tecnologia-industrial",
    "EXP": "expresion-plastica"
}

COMMUNITY = {
    "andalucia": "Andalucía",
    "aragon": "Aragón",
    "asturias": "Asturias",
    "cantabria": "Cantabria",
    "castilla-y-leon": "Castilla y León",
    "castilla-la-mancha": "Castilla-La Mancha",
    "catalunya": "Cataluña",
    "comunidad-valenciana": "Comunidad Valenciana",
    "madrid": "Comunidad de Madrid",
    "extremadura": "Extremadura",
    "uned": "Fuera de España (UNED)",
    "galicia": "Galicia",
    "baleares": "Islas Baleares",
    "canarias": "Islas Canarias",
    "la-rioja": "La Rioja",
    "navarra": "Navarra",
    "pais-vasco": "País Vasco",
    "murcia": "Región de Murcia"
}

ISO_COMMUNITY = {
    "AN": "andalucia",
    "AR": "aragon",
    "AS": "asturias",
    "CB": "cantabria",
    "CL": "castilla-y-leon",
    "CM": "castilla-la-mancha",
    "CT": "catalunya",
    "VC": "comunidad-valenciana",
    "MD": "madrid",
    "EX": "extremadura",
    "UN": "uned",
    "GA": "galicia",
    "IB": "baleares",
    "CN": "canarias",
    "RI": "la-rioja",
    "NA": "navarra",
    "PV": "pais-vasco",
    "MC": "murcia"
}

TITLE = """  ______   ________  __        ________  __        ______    ______   _______   ________  _______  
 /      \ |        \|  \      |        \|  \      /      \  /      \ |       \ |        \|       \ 
|  $$$$$$\| $$$$$$$$| $$      | $$$$$$$$| $$     |  $$$$$$\|  $$$$$$\| $$$$$$$\| $$$$$$$$| $$$$$$$\\
| $$___\$$| $$__    | $$      | $$__    | $$     | $$  | $$| $$__| $$| $$  | $$| $$__    | $$__| $$
 \$$    \ | $$  \   | $$      | $$  \   | $$     | $$  | $$| $$    $$| $$  | $$| $$  \   | $$    $$
 _\$$$$$$\| $$$$$   | $$      | $$$$$   | $$     | $$  | $$| $$$$$$$$| $$  | $$| $$$$$   | $$$$$$$\\
|  \__| $$| $$_____ | $$_____ | $$_____ | $$_____| $$__/ $$| $$  | $$| $$__/ $$| $$_____ | $$  | $$
 \$$    $$| $$     \| $$     \| $$     \| $$     \\$$    $$| $$  | $$| $$    $$| $$     \| $$  | $$
  \$$$$$$  \$$$$$$$$ \$$$$$$$$ \$$$$$$$$ \$$$$$$$$ \$$$$$$  \$$   \$$ \$$$$$$$  \$$$$$$$$ \$$   \$$"""

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def hprint(text):
  print("[" + datetime.datetime.now().strftime("%H:%M:%S") + "] " + text)

def download_pdf(url, path):
  hprint("Requesting " + url)
  hprint("Downloading " + path)
  r = requests.get(url, stream=True)
  file = codecs.open(path, "wb", encoding="utf-8")
  file.write(str(r.content))
  file.close()
  hprint("Downloaded " + path)

async def main():
  print("Initializing scrapper...")
  scrapper: Scrapper = None
  try:
    scrapper = await create_scrapper()
  except Exception as e:
    print("Failed to initialize scrapper. Trying to download binaries... (maybe it's a fresh install)")
    os.system("playwright install chromium")
    try:
      scrapper = await create_scrapper()
    except Exception as e:
      print("Failed to initialize scrapper. Please, check your internet connection and try again.")
      print(e)
      return
  print("Scrapper initialized!")
  
  print("Fetching initial data...")
  await scrapper.goto("https://www.examenesdepau.com/examenes/")
  print("Fetched!")
  cls()
  
  comunidad = "all"
  asignatura = "all"
  año = "all"
  
  examen = True
  criterios = False
  solucion = True
  
  while True:
    cls()
    rprint("[white bold]" + "====================================================================================================")
    rprint("[red bold]" + TITLE)
    rprint("[white bold]" + "====================================================================================================")
    print("")
    rprint("[white bold] Hecho por -- Pol Vallverdú")
    rprint("[white bold] Web -- https://polv.dev")
    rprint("[white bold] Repo -- https://github.com/polvallverdu/seleloader")
    print("")
    print("")
    rprint(f"[orange underline] 1) [white]Seleccionar comunidad autónoma [blue bold]\[[reset blue italic]{comunidad}[blue bold]]")
    rprint(f"[orange underline] 2) [white]Seleccionar asignatura [blue bold]\[[reset blue italic]{asignatura}[blue bold]]")
    rprint(f"[orange underline] 3) [white]Seleccionar año autónoma [blue bold]\[[reset blue italic]{año}[blue bold]]")
    rprint(f"[orange underline] 4) [white]Descargar examen [blue bold]\[[reset blue italic]{examen}[blue bold]]")
    rprint(f"[orange underline] 5) [white]Descargar criterios [blue bold]\[[reset blue italic]{criterios}[blue bold]]")
    rprint(f"[orange underline] 6) [white]Descargar solución [blue bold]\[[reset blue italic]{solucion}[blue bold]]")
    print("")
    rprint(f"[orange underline] 8) [gold bold]Descargar")
    rprint(f"[orange underline] 9) [red bold]Salir")
    print("")
    print("")
    i = input("] ").rstrip()
    cls()
    
    if i == "1":
      rprint("[white]Seleccionar comunidad autónoma:")
      print("")
      for k, v in ISO_COMMUNITY.items():
        rprint(f"[orange underline] {k}) [white]{COMMUNITY[v]}")
      print("")
      comm = input("] ").upper().rstrip()
      if comm == "ALL":
        comunidad = "all"
      else:
        com = ISO_COMMUNITY.get(comm) if comm in ISO_COMMUNITY else None
        if com is not None:
          comunidad = com
    elif i == "2":
      rprint("[white]Seleccionar asignatura, o ponga \"all\":")
      print("")
      for k, v in SIMPLE_SUBJECTS.items():
        rprint(f"[orange underline] {k}) [white]{SUBJECTS[v]}")
      print("")
      subj = input("] ").upper().rstrip()
      if subj == "ALL":
        asignatura = "all"
      else:
        sub = SIMPLE_SUBJECTS.get(subj) if subj in SIMPLE_SUBJECTS else None
        if sub is not None:
          asignatura = sub
    elif i == "3":
      rprint("[white]Seleccionar el año deseado, o ponga \"all\":")
      print("")
      year = input("] ").rstrip()
      if year == "all":
        año = year
      else:
        try:
          int(year)
          año = year
        except:
          pass
    elif i == "4":
      examen = not examen
    elif i == "5":
      criterios = not criterios
    elif i == "6":
      solucion = not solucion
    elif i == "8":
      hprint("Navigating to url ")
      # Formatting url
      url = "https://www.examenesdepau.com/examenes/"
      if comunidad != "all":
        url += f"{comunidad}/"
      if asignatura != "all":
        url += f"{asignatura}/"
      if año != "all":
        url += f"{año}/"
        
      hprint(f"Navigating to url {url}")
      await scrapper.goto(url) # TODO: Pagination
      hprint(f"Scrapping exams")
      results = await scrapper.extract_exam_data() 
      
      # Generating all tasks
      for res in results:
        sss = res["location"] + "/" + res["subject"]
        path = f"downloads/{sss}" + "/" + res["date"] 
        os.makedirs(f"downloads/{sss}", exist_ok=True)
        uid = res["id"]
        
        if examen:
          finalpath = f"{path}_examen.pdf"
          if os.path.exists(finalpath):
            continue
          download_pdf(f"https://www.examenesdepau.com/files/examen/{uid}/", finalpath)
        if criterios:
          finalpath = f"{path}_criterios.pdf"
          if os.path.exists(finalpath):
            continue
          download_pdf(f"https://www.examenesdepau.com/files/criterios/{uid}/", finalpath)
        if solucion:
          finalpath = f"{path}_solucion.pdf"
          if os.path.exists(finalpath):
            continue
          download_pdf(f"https://www.examenesdepau.com/files/solucion/{uid}/", finalpath)
        
        await asyncio.sleep(1.12)
      
      rprint("[green bold]Done!")
      await asyncio.sleep(3)
    elif i == "9":
      break

  print("Shutting down scrapper...")
  await scrapper.shutdown()
  exit(1)
  
if "__main__" == __name__:
  asyncio.run(main())