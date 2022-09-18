<script lang="ts">
  import { time } from './stores'
  import Table from './Table.svelte'

  export let schedule: Object
  export let name: string

  const keys: Array<string> = schedule['keys']

  function initKey(time: Date, keys: Array<string>): string {
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
  const routeMapUrl: string = schedule[""]

  let currentKey = initKey($time, keys)
  $: currentSchedule = schedule[currentKey]
</script>

<div>
  <h3>
    <a href={'srcUrl' in schedule ? schedule['srcUrl'] : './'}>
      {name} 
    </a>
    {#if 'routeMapUrl' in schedule}
      (<a href={schedule['routeMapUrl']}>Route Map</a>)
    {/if}
  </h3>

  <form>
    <select bind:value={currentKey}>
      {#each keys as key}
        <option value={key}>{key}</option>
      {/each}
    </select>
  </form>

  <Table data={currentSchedule} />
</div>

<style>
  a {
    text-decoration: underline;
    color: inherit;
  }
</style>
