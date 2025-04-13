function decimalValidator () {
  return function decimal (value) {
    return (value && !!value.match(/^[+-]?((?:0|[1-9][0-9]{0,2}(?: [0-9]{3})*)|(\d+))[\.,]?\d*$/)) || 'Please enter a valid decimal number'
  }
}

function requiredValidator () {
  return function required (value) {
    return (value !== undefined && value !== null && value !== '') || 'This field is required'
  }
}

export {
  decimalValidator,
  requiredValidator
}
