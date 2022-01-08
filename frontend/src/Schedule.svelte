<script lang="ts">
  import Table from './Table.svelte'
  // import Radio from './Radio.svelte'

  export let schedule: Object
  export let name: string
  export let time: Date

  const keys: Array<string> = schedule['keys']
//   const options = keys.map((key) => {
//     return {
//       value: key,
//       label: key,
//     }
//   })

  /*let radioValue = keys[0]*/
  /*$: currentSchedule = schedule[radioValue]*/

  function initKey(): string {
    let currentKey = keys[0]
    const isWeekend = time.getDay() === 6 || time.getDay() === 0
    if (isWeekend) {
        const re = /weekend|Weekend|saturday|Saturday/
        const newKey = keys.find((k) => k.match(re))
        currentKey = newKey ? newKey : currentKey
    } else {
        const re = /weekday|Weekday/
        const newKey = keys.find((k) => k.match(re))
        currentKey = newKey ? newKey : currentKey
    }

    if (time < new Date('2022-01-17T00:00:00')) {
      // Winter break time
      const re = /break|Break/
      const newKey = keys.find((k) => k.match(re))
      currentKey = newKey ? newKey : currentKey
    }
    return currentKey
  }

  let currentKey = initKey()
  $: currentSchedule = schedule[currentKey]
  

</script>

<div>
  <a href={'srcUrl' in schedule ? schedule['srcUrl'] : './'}>
    <h3>{name}</h3>
  </a>
  <span>Schedule: {currentKey}</span>

  <!-- <Radio
    {options}
    fontSize={16}
    bind:userSelected={radioValue}
  /> -->
  <Table data={currentSchedule} bind:currentTime={time} />
</div>

<style>
  a {
    text-decoration: underline;
    color: inherit;
  }
</style>
