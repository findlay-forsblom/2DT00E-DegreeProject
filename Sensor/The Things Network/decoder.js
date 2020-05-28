function Decoder(bytes, port) {
  // Decode an uplink message from a buffer
  // (array) of bytes to an object of fields.
  var decoded = {};
  
function uintToString(uintArray) {
    var encodedString = String.fromCharCode.apply(null, uintArray),
        decodedString = decodeURIComponent(escape(encodedString));
    return decodedString;
}

  val = uintToString(bytes)
  split_val = val.split(',')
  if(split_val[0].substring(0,3) === 'ack'){
    decoded.values = val
  }
  else{
    decoded.temp = split_val[0]
    decoded.humid = split_val[1]
    decoded.depth = split_val[2]
    decoded.pitch = split_val[3]
    decoded.values = val
  }

  return decoded;
}