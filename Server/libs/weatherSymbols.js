const symbols = [
  { id: 1, type: 'Clear sky', type_se: 'Klart', icon: '1.png' },
  { id: 2, type: 'Nearly clear sky', type_se: 'Lätt molnighet', icon: '2.png' },
  { id: 3, type: 'Variable cloudiness', type_se: 'Halvklart', icon: '3.png' },
  { id: 4, type: 'Halfclear sky', type_se: 'Molnigt', icon: '4.png' },
  { id: 5, type: 'Cloudy sky', type_se: 'Mycket moln', icon: '5.png' },
  { id: 6, type: 'Overcast', type_se: 'Mulet', icon: '6.png' },
  { id: 7, type: 'Fog', type_se: 'Dimma', icon: '7.png' },
  { id: 8, type: 'Light rain showers', type_se: 'Lätt regn', icon: '8.png' },
  { id: 9, type: 'Moderate rain showers', type_se: 'Regn', icon: '9.png' },
  { id: 10, type: 'Heavy rain showers', type_se: 'Kraftigt regn', icon: '10.png' },
  { id: 11, type: 'Thunderstorm', type_se: 'Åskskur', icon: '11.png' },
  { id: 12, type: 'Light sleet showers', type_se: 'Lätt by av regn och snö', icon: '12.png' },
  { id: 13, type: 'Moderate sleet showers', type_se: 'By av regn och snö', icon: '13.png' },
  { id: 14, type: 'Heavy sleet showers', type_se: 'Kraftig by av regn och snö', icon: '14.png' },
  { id: 15, type: 'Light snow showers', type_se: 'Lätt snöby', icon: '15.png' },
  { id: 16, type: 'Moderate snow showers', type_se: 'Snöby', icon: '16.png' },
  { id: 17, type: 'Heavy snow showers', type_se: 'Kraftig snöby', icon: '17.png' },
  { id: 18, type: 'Light rain', type_se: 'Lätt regn', icon: '18.png' },
  { id: 19, type: 'Moderate rain', type_se: 'Regn', icon: '19.png' },
  { id: 20, type: 'Heavy rain', type_se: 'Kraftigt regn', icon: '20.png' },
  { id: 21, type: 'Thunder', type_se: 'Åska', icon: '21.png' },
  { id: 22, type: 'Light sleet', type_se: 'Lätt snöblandat regn', icon: '22.png' },
  { id: 23, type: 'Moderate sleet', type_se: 'Snöblandat regn', icon: '23.png' },
  { id: 24, type: 'Heavy sleet', type_se: 'Kraftigt snöblandat regn', icon: '24.png' },
  { id: 25, type: 'Light snowfall', type_se: 'Lätt snöfall', icon: '25.png' },
  { id: 26, type: 'Moderate snowfall', type_se: 'Snöfall', icon: '26.png' },
  { id: 27, type: 'Heavy snowfall', type_se: 'Ymnigt snöfall', icon: '27.png' }
]

function getSymbol (forecast) {
  const cast = []
  forecast.forEach(forecast => {
    // Find right symbol to forecast.
    const symbol = symbols.filter(symb => {
      // return symb.id === forecast.params[4].values[0]
      return symb.id === forecast.commonSymbol
    })

    // Push filtered forecast to array.
    // cast.push({
    //   temp: forecast.params[0].values[0],
    //   humid: forecast.params[1].values[0],
    //   symb: symbol[0],
    //   date: forecast.date
    // })
    forecast.symb = symbol[0]
    cast.push(forecast)
  })

  return cast
}

module.exports = { symbols: symbols, getSymbol }
