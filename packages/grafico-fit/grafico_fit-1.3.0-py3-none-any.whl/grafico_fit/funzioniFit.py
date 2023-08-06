"""
Libreria per fare grafici di fit e tabelle LaTeX a partire da dati raccolti in un file Excel

TODO: aggiungere comandi extra prima di salvere il grafico (not working)
"""
__docformat__="numpy"

import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd
from pint import UnitRegistry
import re

def _tex_escape(text):
    """
        :param text: a plain text message
        :return: the message escaped to appear correctly in LaTeX
    """
    conv = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
        '<': r'\textless{}',
        '>': r'\textgreater{}',
    }
    regex = re.compile('|'.join(re.escape(str(key)) for key in sorted(conv.keys(), key = lambda item: - len(item))))
    return regex.sub(lambda match: conv[match.group()], text)

def _converti_latex(text):
    ureg = UnitRegistry()
    um=re.search(r"\[(.+)\]",text).group(1) #ricerca unità di misura
    u=ureg.Unit(um)
    um_tex=f"{u:Lx}"
    new_text=text.replace("["+um+"]","[]") #cancellazione unità di misure
    new_text=_tex_escape(new_text) 
    new_text=new_text.replace("[]",r"\(\left["+um_tex+r"\right]\)") #inserimento siunix dopo aver fatto l'escape dei caratteri speciali per latex
    return new_text

def _do_extra(to_do):
    code_to_execute = compile("\n".join(to_do), "<string>", "exec")
    exec(code_to_execute)

def fit(file_name,file_result,variabile_x,variabile_y,sigma_y,f_fit,titoli_p_latex,
    split_graphs=False,
    titoli=["",""],
    xlabel=None,
    ylabel=None,
    path=".",
    xscale="linear",
    yscale="linear",
    griglia_fit={
        "which" : "both",
        "ls" : "dashed",
        "color" : "gray"
    },
    griglia_residui={
        "which" : "both",
        "ls" : "dashed",
        "color" : "gray"
    },
    style_fit={"fmt" : "o"},
    style_residui={"fmt" : "o"},
    foglio="Foglio1",
    aggiunte=["a=1","print(a)","print(foglio)"]
):
    """
    funzione che genera:

        - un pdf:

            - contenente il grafico di fit e quello dei residui

        - un file LaTeX:
        
            - contenete i parametri ottimali del fit
    
    Parameters
    -------------------------
    file_name : str
        nome file excel da elaborare

    file_result : str
        nome da dare ai pdf generati

    variable_x, variable_y, sigma_y : str
        ogni parametro contine il valore dell'header della colonna del foglio excel da cui prendere i dati
        (deve contenere l'unità di misura nel formato: "[unità di misura]")

    f_fit : func
        funzione che rappresenta la curva g(x) utilizzata nel fit.
        il primo parametro di f è x, gli altri sono tutti i parametri che definiscono g(x)

    titoli_p_latex : list
        elenco dei nomi dei parametri ottimali che vengono ricavati dal fit
        verranno usati come contenuto della cella del titolo di una tabella latex contenente i valori numerici dei parametri

    split_graphs: bool, optional
        se True la funzione genera due file separati per il grafico dei residui e il grafico di fit (default: False)

    titoli : list, optional
        lista di due elementi con i due titoli per i due grafici, il primo è il grafico di fit e il secondo è il grafico dei 
        residui (default: ["",""])
    
    xlabel, ylabel : str, optional
        stringa da utilizzare per la generazione dei label del grafico, usare notezione LaTeX. Se ==None allora i nomi delle colonne
        del file excel verranno utilizzati, convertendo automaticamente in LaTeX (default: None)

    path : str, optional
        path directory di partenza (default: ".")

    xscale, yscale : str, optional
        tipo di scala da utilizzare per l'asse corrispondente del grafico (default: 'linear')

    griglia_fit, griglia_residui : dict, optional
        dizionario contenente i parametri opzionali da passare a pyplot.grid() (default: {"which" : "both", "ls" : "dashed", "color" : "gray"})

    style_fit, style_residui : dict, optional
        dizionario contenente i parametri opzionali da passare a pyplot.errorbar() (default: {"fmt" : "o"})

    foglio : str, optional
        nome del foglio da cui prendere i dati (default: "Foglio1")

    aggiunte : list, optional
        lista di comandi da eseguire prima che il grafico venga salvato, usare ax1 per modificare il grafico di fit, ax1 per modificare
        il grafico dei residui. nel caso di split_graphs=True le modifiche vengono apllicate al grafico dei residui (non usare ax1 e ax2 in questo caso)

    Examples
    ----------------------------
    >>> def retta(x,m,q):
            return m*x+q
        result="nome grafico"
        file="moto_rettilineo.xlsx"
        var_x="tempi [s]"
        var_y="posizioni [cm]"
        sigma_y="incertezza posizione [cm]"
        titoli=["\\hat{m} [\\si{\\centi\\metre\\per\\second}]", "\\hat{q} [\\si{\\centi\\metre}]"]
        result=fit(file,result,var_x,var_y,sigma_y,retta,titoli)
        if result:
            print(result)
    
    oppure usando la funzione del pendolo fisico che utilizza un solo parametro:
    >>> def pendolo(d, l):
            return 2.0 * np.pi * np.sqrt((l**2.0 / 12.0 + d**2.0) / (9.81 * d))
        result="nome grafico"
        file="pendolo.xlsx"
        var_x="lunghezze [m]"
        var_y="tempi_medi [s]"
        sigma_y="sigma_t [s]"
        titoli_pendolo=["\\hat{l} [\\si{\\metre}]"]
        result=fit(file,result,var_x,var_y,sigma_y,pendolo,titoli_pendolo)
        if result:
            print(result)

    oppure passando parametri opzionali:
    >>> def retta(x,m,q):
            return m*x+q
        my_path="C:\\Users\\cremo\\Documents\\Università\\Relazioni"
        res="nome grafico"
        file="moto_rettilineo.xlsx"
        x="tempi [s]"
        y="posizioni [cm]"
        s_y="incertezza posizione [cm]"
        titoli=["\\hat{m} [\\si{\\centi\\metre\\per\\second}]", "\\hat{q} [\\si{\\centi\\metre}]"]
        asse_y="log"
        style={"ls" : "dotted", "color" : "green"}
        result=fit(file,res,x,y,s_y,retta,titoli,yscale=asse_y,griglia_fit=style, path=my_path)
        if result:
            print(result)
    """

    #verifica parametri
    if "[" not in variabile_x or "]" not in variabile_x: 
        return "Manca unità di misura in x"
    if "[" not in variabile_y or "]" not in variabile_y:
        return "Manca unità di misura in y"
    if "[" not in sigma_y or "]" not in sigma_y:
        return "Manca unità di misura in dy"
    if not file_name:
        return "specificare nome file excel"
    if not file_result:
        return "specificare nome file pdf risultato (senza .pdf)"

    #lettura file
    excel = pd.read_excel(path+'\\'+file_name, sheet_name=foglio)

    t=[e for e in excel[variabile_x].tolist() if e == e] #NaN != NaN quindi il test impedisce di scrivere i valori nulli
    y=[e for e in excel[variabile_y].tolist() if e == e]
    dy=[e for e in excel[sigma_y].tolist() if e == e]

    print(t,y,dy)

    #fit
    popt, pcov = curve_fit(f_fit,t,y,sigma=dy)
    
    #scrittura file_tabella.tex
    empty_space="&"*(len(popt)-1)+"\\\\" #linee vuote per aggiungere spazio prima e dopo in ogni riga
    lines_prima=["\\renewcommand{\\arraystretch}{0.5}","\\begin{table}[h!]","\\centering"]
    colonne="c"*len(popt) #colonne centrate in numero variaabile a seconda di len(popt)
    lines_prima.append("\\begin{tabular}{"+colonne+"}")
    lines_prima.append("\\toprule")
    lines_prima.append(empty_space)
    lines_prima.append(' & '.join(titoli_p_latex)+' \\\\')#titoli
    lines_prima.append(empty_space)
    lines_prima.append("\\midrule")
    lines_prima.append(empty_space)
    string_popt=[str(i_opt) for i_opt in popt] #numeri convertiti in stringa
    lines_prima.append(' & '.join(string_popt)+' \\\\') #valori
    lines_prima.append(empty_space)
    lines_dopo=["\\bottomrule","\\end{tabular}","\\caption{risultati del fit}","\\end{table}","\\renewcommand{\\arraystretch}{1}"]
    lines_prima.extend(lines_dopo)    
    
    with open(path+"\\"+file_result+"_tabella.tex", 'w') as tabella_tex:
        tabella_tex.write("\n".join(lines_prima))
        tabella_tex.close()

    #disegno grafico 
    pad=(max(t)-min(t))/20
    a = np.linspace(min(t)-pad if min(t)-pad>0 else 0, max(t)+pad, 1001)

    plt.rcParams.update({"text.usetex" : True, 
        "font.family": "computer modern",
        "text.latex.preamble": "\n".join([ # plots will use this preamble
        r"\usepackage[utf8]{inputenc}",
        r"\usepackage[T1]{fontenc}",
        r"\usepackage{siunitx}",
        ])})
    
    if split_graphs:
        #grafico fit
        plt.figure(file_result)
        plt.title(titoli[0])
        if xlabel != None:
            plt.xlabel(xlabel)
        else:
            plt.xlabel(_converti_latex(variabile_x))
        if ylabel != None:
            plt.ylabel(ylabel)
        else:
            plt.ylabel(_converti_latex(variabile_y))
        plt.xscale(xscale)
        plt.yscale(yscale)
        plt.grid(**griglia_fit)
        plt.errorbar(t, y, dy, **style_fit)
        plt.plot(a, f_fit(a, *popt)) # l'asterisco indica che popt viene espanso passando i parametri singolarmente e non come lista.
        plt.savefig(path+'\\'+file_result+'.pdf')

        #disegno grafico dei residui
        plt.figure('Residui')
        plt.title(titoli[1])
        plt.xlabel(_converti_latex(variabile_x))
        plt.ylabel(_converti_latex(variabile_y))
        plt.grid(**griglia_residui)
        y_res=y-f_fit(np.array(t), *popt)  # l'asterisco indica che popt viene espanso passando i parametri singolarmente e non come lista.
        plt.errorbar(t, y_res, dy, **style_residui)
        plt.plot(a,a-a)
        plt.savefig(path+'\\'+file_result+'_residui.pdf')
    else:
        #fit subplot
        fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [4, 1]}, sharex=True)
        ax1.set_title(titoli[0])
        ax1.set_xscale(xscale)
        ax1.set_yscale(yscale)
        ax1.grid(**griglia_fit)
        ax1.errorbar(t, y, dy, **style_fit)
        ax1.plot(a, f_fit(a, *popt)) # l'asterisco indica che popt viene espanso passando i parametri singolarmente e non come lista.
        
        #residui subplot
        ax2.set_title(titoli[1])
        ax2.margins(0, 0.2)
        ax2.set_xscale(xscale)
        ax2.set_yscale(yscale)
        ax2.grid(**griglia_residui)
        y_res=y-f_fit(np.array(t), *popt)  # l'asterisco indica che popt viene espanso passando i parametri singolarmente e non come lista.
        ax2.errorbar(t, y_res, dy, **style_residui)
        ax2.plot(a, a-a)
        ##adjust for x axi symmetry
        low, high = ax2.get_ylim() 
        bound = max(abs(low), abs(high)) # find the new limits
        ax2.set_ylim(-bound, bound) # set new limits

        #labels
        if xlabel != None:
            fig.supxlabel(xlabel, y=0.05)
        else:
            fig.supxlabel(_converti_latex(variabile_x), y=0.05)
        if ylabel != None:
            fig.supylabel(ylabel, x=0.03)
        else:
            fig.supylabel(_converti_latex(variabile_y), x=0.03)
        
        fig.tight_layout()

        fig.savefig(path+'\\'+file_result+'.pdf')
        fig.canvas.manager.set_window_title("Grafico") 
        
    plt.show()

def tabella(file_name,file_result,
    path=".",
    colonne=None,
    foglio="Foglio1",
    index_on=False,
    formatter=None,
    column_align=None,
    table_caption="Tabella di dati"
):
    """
    funzione che crea una tabella in LaTeX a partire da dati in un file Excel.

    le unità di misura devono essere riportaate per ogni colonna tra parentesi quadre.

    Parameters
    -------------------------
    file_name : str
        nome file excel da elaborare

    file_result : str
        nome da dare alle tabelle generate

    path : str, optional
        path directory di partenza (default: ".")

    colonne : list, optional
        lista contenete i valori degli header delle colonne del foglio excel da cui prendere i dati
        (default: None, che corrisponde a selezionare tutte le colonne)

    foglio: str, optional
        indica il nome del foglio da cui prendere i dati (default: "Foglio1")

    index_on: bool, optional
        decide se mostrare l'indice di riga (default: False)

    formatter: dict, optional
        dizionario contenente laa funzione per formattare i valori della tabella. I valori del dizionario usano come chiave il nome
        della colonna e come volore la funzione che formatta(default: None)

    column_align: str, optional
        stringa contenete il formato delle colonne, il formato stringa deve essere stile LaTeX, ad esempio "||l|c|r||" (default: None)

    table_caption: str, optional
        label da posizionare sotto alla tabella generata (default: "Tabella di dati")

    Examples
    ----------------------------
    >>> my_path="C:\\Users\\cremo\\Documents\\Università\\Relazioni\\pendolo_json"
        file_result="nome_grafico"
        file_tabella="nome_tabella"
        file_name="prova_json.xlsx"
        formati={
            "tempi_medi [s]": "{:.4f}".format,
            "sigma_t [s]": "{:.9f}".format,
            "lunghezze [m]": "{:.3f}".format
        }
        result=js.tabella(file_name,file_tabella, formatter=formati, path=my_path)
        if result:
            print(result)
    """
    #lettura file
    excel = pd.read_excel(path+'\\'+file_name, sheet_name=foglio, usecols=colonne)
    #scrittura file
    ##creazione header in stile LaTeX
    my_header=[]
    for col in excel.columns:
        new_col=_converti_latex(col)
        my_header.append(new_col)

    latex = excel.to_latex(
        buf=path+"\\"+file_result+".tex",
        index=index_on,
        formatters=formatter,
        column_format=column_align,
        decimal=",", #separatore decimale
        longtable=True, #tipo di tabeòòa
        caption=table_caption,
        na_rep="", #carattere da mettere nei posti NaN
        header=my_header,
        escape=False #impedisce escape latex special char
    )


