import speedtest

st = speedtest.Speedtest()



def checksp(speed):
    print('Testing internet speed...')
    try:
        print(f'Download speed is: {speed.download()/1000000:.1f} Mbps')
        print(f'Upload speed is: {speed.upload()/1000000:.1f} Mbps')
    except KeyboardInterrupt:
            print('\n\n[!] Test cancelled by user')
            exit()


checksp(st)
