for n in range(2,21):
    with open(f'multi\multi_{n}.txt','w') as f:
        for i in range(1,21):
            content=f'{n} x {i} = {n*i}\n'
            f.write(content)
