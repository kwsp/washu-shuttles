<script lang="ts">
  import { onMount } from 'svelte'
  export let data: Schedule
  export let currentTime: Date

  interface Schedule {
    [stop: string]: Array<string | null>
  }
  const schedule: Schedule = data

  if (data == undefined) {
    console.log('warning: table data undefined')
  }

  // if ordered keys provided, use that
  const keys: Array<string> = data['keys'] || Object.keys(data)

  function parseTime(s: string): Date {
    const res = s.match(/(1[0-2]|0?[1-9]):([0-5][0-9]) ?([AaPp][Mm])/)
    if (!res) {
      return new Date()
    }
    const hour = parseInt(res[1])
    const minute = parseInt(res[2])
    const ampm = res[3]

    const d = new Date()
    d.setMinutes(minute)
    if (ampm.match(/[Pp][Mm]/)) {
      // PM
      d.setHours((hour % 12) + 12)
    } else {
      // AM
      d.setHours(hour)
      if (hour < 5 || hour == 12) {
        d.setDate(d.getDate() + 1)
      }
    }
    return d
  }

  // Bisect the array given a predicate
  // Check the element after the first one found to make sure
  // there isn't a mistake. Otherwise, AM/PM typos will mess it up.
  function bisect(
    arr: Array<string>,
    fn: (arg0: string | null) => Boolean
  ): number {
    const i = arr.findIndex((v) => fn(v))
    if (i == -1) {
      return arr.length
    }
    if (!isFuture(arr[i + 1])) {
      return i + 1 + bisect(arr.slice(i + 1), fn)
    }
    return i
  }

  function bisectAll(schedule: Schedule) {
    const indices = {}
    for (const key of keys) {
      indices[key] = bisect(schedule[key], isFuture)
    }
    return indices
  }

  const bisectIndices = bisectAll(schedule)

  // Predicate to check if this bus will arrive in the future
  function isFuture(entry: string | null): Boolean {
    return entry ? currentTime < parseTime(entry) : false
  }

  // get CSS class based on time to determine highlight
  function getClass(key: string, i: number): string {
    return i >= bisectIndices[key] ? 'highlight' : ''
  }

  let nowElems = {}
  onMount(() => {
    keys.forEach((key) => nowElems[key] && nowElems[key].scrollIntoView())
  })
</script>

<div class="table-container">
  <table>
    <tbody>
      {#each keys as key}
        <tr>
          <th class="fixed">{key}</th>
          {#each schedule[key] as entry, i}
            {#if i == bisectIndices[key]}
              <td class="highlight" bind:this={nowElems[key]}>{entry}</td>
            {:else if i > bisectIndices[key]}
              <td class="highlight">{entry}</td>
            {:else}
              <td>{entry}</td>
            {/if}
          {/each}
        </tr>
      {/each}
    </tbody>
  </table>
</div>

<style>
  .table-container {
    width: 100%;
    overflow: scroll;
  }

  table {
    text-align: center;
    border-collapse: collapse;
    border-top: 1px solid grey;
  }

  th,
  td {
    white-space: nowrap;
    padding: 5px 10px;
    font-family: Arial;
    border: 1px solid grey;
  }

  th:first-child,
  td:first-child {
    position: sticky;
    width: 100px;
    left: 0;
    z-index: 10;
    background: #fff;
  }

  tr th:first-child {
    z-index: 11;
  }

  tr th {
    position: sticky;
    top: 0;
    z-index: 9;
    background: #fff;
  }

  td,
  th {
    text-align: left;
    vertical-align: top;
    padding: 5px 10px;
    margin: 0;
    border: 1px solid grey;
    white-space: nowrap;
    border-top-width: 0px;
  }

  tbody tr {
    border-bottom: 1px solid #dddddd;
  }

  tbody tr:nth-of-type(even) {
    background-color: #f8f8f8;
  }

  .highlight {
    background-color: rgb(138, 202, 132);
  }
</style>
