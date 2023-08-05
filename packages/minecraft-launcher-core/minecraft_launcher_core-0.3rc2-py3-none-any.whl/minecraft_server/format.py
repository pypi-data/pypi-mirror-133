

class Format:
    def __init__(self):
        pass
    def decode(self,st):
        civ = {}
        for i in st.split('\n'):
            civ[i.split('=')[0]] = i.split('=')[1]
        return civ
    def encode(self,dic=dict):
        st = ''
        for i in dic.items():
            st += f'{i[0]}={i[1]}\n'
        print(st)



