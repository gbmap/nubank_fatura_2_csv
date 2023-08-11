from argparse import ArgumentParser
import os
import re
import fitz

def fatura2csv(fname:str) -> str:
    s = ['Data,Descricao,Valor']
    with fitz.open(fname) as f:
        for i in range(3,max(4,len(f))):
            w = [t[4].split('\n') for t in f[i].get_text("blocks") if re.match(r'\d{2}',t[4])]
            w = [x1+x2 for x1,x2 in zip(w, w[1:]+[w[-1]]) if re.match(r'\d{2}\s\w{3}',x1[0])] # lidar com conversão de compra internacional
            w = list(map(lambda x:(x[0],x[1],x[2-4*(not x[2][0].isdigit())].replace(',','.')), w))
            w2m = dict(zip(['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ'], range(1,13)))
            s = s+[','.join([f'{x[0][:2]}/{w2m[x[0][3:6]]:02}',*x[1:]]) for x in w] # converte mes
    return '\n'.join(s)

def main():
    parser = ArgumentParser()
    parser.add_argument('-f', '--filename', help='.pdf da fatura. (ou pasta)', required=True)
    args = parser.parse_args()

    fname = args.filename
    dname = os.path.dirname(fname)
    fs = [fname] if not os.path.isdir(fname) else [os.path.join(dname,n) for n in os.listdir(fname) if n.endswith('pdf')]
    for n in fs:
        with open(n.replace('.pdf', '.csv'), 'w') as f:
            f.write(fatura2csv(n))
    print('só contar as moeda agora')


if __name__ == '__main__':
    main()