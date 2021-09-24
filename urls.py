from controllers import *
 
 
# FastAPIのルーティング用関数
app.add_api_route('/', index)
app.add_api_route('/admin', admin)
app.add_api_route('/register', register, methods=['GET', 'POST'])
app.add_api_route('/play', play, methods=['GET', 'POST'])
app.add_api_route('/delete/{t_id}', delete)