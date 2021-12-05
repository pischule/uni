<script>

	import Big from 'big.js'

	import { decimalValidator, requiredValidator } from './validators.js'
  	import { createFieldValidator } from './validation.js'

  	const [ validityA, validateA ] = createFieldValidator(requiredValidator(), decimalValidator());
	const [ validityB, validateB ] = createFieldValidator(requiredValidator(), decimalValidator());

	const urlParams = new URLSearchParams(window.location.search);

	let total = Big(0).toFixed(6);
	let a = Big(0).toFixed(6);
	let b = Big(0).toFixed(6);
	let operation = '+';

	function updateResult() {
		if (!$validityA.valid || !$validityB.valid) {
			return;
		}

		const aNumber = a.replace(/,| /g, '');
		const bNumber = b.replace(/,| /g, '');
		if (operation === '+') {
			total = Big(aNumber).plus(bNumber);
		} else if (operation === '-') {
			total = Big(aNumber).minus(bNumber);
		} else if (operation === '*') {
			total = Big(aNumber).times(bNumber);
		} else if (operation === '/') {
			if (Big(0).eq(bNumber)) {
				alert('You cannot divide by zero');
				return;
			}
			total = Big(aNumber).div(bNumber);
		}

		total = total.toFixed(6);
	}
	
	function numberWithCommas(x) {
		let str = x.split('.');
    	str[0] = str[0].replace(/\B(?=(\d{3})+(?!\d))/g, " ");
		return str.join('.');
	}

</script>

<h1>Калькулятор</h1>
<p>
	Студент: {urlParams.get('student') || 'Пищулёнок Максим Сергеевич'}<br>
	Курс: {urlParams.get('course') || '4'}<br>
	Группа: {urlParams.get('group') || '4'}<br>
	Год: {new Date().getFullYear()}
</p>

<input class="input"
type="text"
bind:value={a}
on:input={updateResult}
class:field-danger={!$validityA.valid}
class:field-success={$validityA.valid}
use:validateA={a}
/>

<label>
	<input type=radio class="btn-check" bind:group={operation} on:change={updateResult} name="operation" value={"+"}>+ 
	<input type=radio bind:group={operation} on:change={updateResult} name="operation" value={"-"}>- 
	<input type=radio bind:group={operation} on:change={updateResult} name="operation" value={"*"}>* 
	<input type=radio bind:group={operation} on:change={updateResult} name="operation" value={"/"}>/ 
</label>

<input class="input"
type="text"
bind:value={b}
on:input={updateResult}
class:field-danger={!$validityB.valid}
class:field-success={$validityB.valid}
use:validateB={b}
/>

<p>Result:</p>
<input class="input" type=text value={numberWithCommas(total)} readonly=True> 

<style>
	:global(body) {
		display: flex;
		flex-direction: column;
	}

	input {
		outline: none;
		border-width: 2px;
	}
	
	.field-danger {
		border-color: red;
	}
	
	.field-success {
		border-color: green;
	}
</style>
