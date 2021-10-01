positions = 0

def position(now_position, plus_number, positions, data):
  positions = now_position
  positions += plus_number
  if now_position + plus_number == 8 \
    or now_position + plus_number == 20:
    data.position = str(now_position + plus_number+1)
    data.remain = str(24-(now_position + plus_number+1))
    positions += 1
    lucky_number = '+1'

  elif now_position + plus_number == 1 \
    or now_position + plus_number == 5 \
      or now_position + plus_number == 12 \
        or now_position + plus_number == 15:
        data.position = str(now_position + plus_number+2)
        data.remain = str(24-(now_position + plus_number+2))
        positions += 2
        lucky_number = '+2'

  elif now_position + plus_number == 18:
    data.position = str(now_position + plus_number-1)
    data.remain = str(24-(now_position + plus_number-1))
    positions -= 1
    lucky_number = '-1'
                
  elif now_position + plus_number == 6 \
    or now_position + plus_number == 13 \
      or now_position + plus_number == 23:
      data.position = str(now_position + plus_number-2)
      data.remain = str(24-(now_position + plus_number-2))
      positions -= 2
      lucky_number = '-2'
            
  elif now_position + plus_number == 22:
    data.position = str(0)
    data.remain = str(24)
    lucky_number = 'スタートへ戻る'
            
  else:
    data.position = str(now_position + plus_number)
    data.remain = str(24-(now_position + plus_number))
    lucky_number = ''

  return data, positions, lucky_number