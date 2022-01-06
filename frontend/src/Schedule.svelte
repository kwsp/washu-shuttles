<script lang="ts">
  import Table from './Table.svelte'

  export let schedule: Object
  export let name: string
  export let time: Date
  
  let keys = schedule['keys']

</script>

<div>
  <a href={'srcUrl' in schedule ? schedule['srcUrl'] : './'}>
    <h3>{name}</h3>
  </a>
  <p>{keys}</p>
  <Table data={schedule[keys[0]]} currentTime={time} />
</div>

<style>

  a {
    text-decoration: underline;
    color: inherit;
  }
</style>