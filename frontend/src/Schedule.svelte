<script lang="ts">
  import Table from './Table.svelte'
  // import Radio from './Radio.svelte'

  export let schedule: Object
  export let name: string
  export let time: Date
  export let breakEndDate: Date = new Date('2022-01-31T00:00:00')

  const keys: Array<string> = schedule['keys']
  //   const options = keys.map((key) => {
  //     return {
  //       value: key,
  //       label: key,
  //     }
  //   })

  /*let radioValue = keys[0]*/
  /*$: currentSchedule = schedule[radioValue]*/

  function initKey(time: Date, keys: Array<string>): string {
    if (time < breakEndDate) {
      // Check if break schedule first.
      const re = /break/i
      const key = keys.find((k) => k.match(re))
      if (key) {
        return key
      }
    }

    let re = /weekday/i
    switch (time.getDay()) {
      case 6:
        re = /weekend|saturday/i
        break
      case 0:
        re = /weekend|sunday/i
        break
    }

    const newKey = keys.find((k) => k.match(re))
    return newKey ? newKey : keys[0]
  }

  let currentKey = initKey(time, keys)
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
