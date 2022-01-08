<script lang="ts">
  import { afterUpdate } from 'svelte'
  export let data: Schedule
  export let currentTime: Date

  interface Schedule {
    [stop: string]: Array<string | null>
  }

  let keys: Array<string>
  $: keys = data['keys'] || Object.keys(data)

  // Predicate to check if this bus will arrive in the future
  function isFuture(entry: string | null, now: Date): Boolean {
    return entry ? now < parseTime(entry) : false
  }

  function parseTime(s: string): Date {
    const time = new Date()
    const match = s.match(/(1[0-2]|0?[1-9]):([0-5][0-9]) ?([AaPp][Mm])/)
    if (!match) {
      return time
    }

    const hour = parseInt(match[1])
    const minute = parseInt(match[2])
    const ampm = match[3]

    time.setMinutes(minute)
    if (ampm.match(/[Pp][Mm]/)) {
      // PM
      time.setHours((hour % 12) + 12)
    } else {
      // AM
      time.setHours(hour)
      if (hour < 5 || hour == 12) {
        time.setDate(time.getDate() + 1)
      }
    }
    return time
  }

  /**
   * Given an array and a predicate, return the index of the element that satisfies the predicate.
   * Checks the element after the first one found to make sure there isn't a mistake.
   * Otherwise, AM/PM typos in the data will mess it up.
   */
  function bisect(
    arr: Array<string>,
    fn: (arg0: string | null) => Boolean
  ): number {
    const i = arr.findIndex((v) => fn(v))
    if (i == -1) {
      return arr.length
    }
    if (!fn(arr[i + 1])) {
      return i + 1 + bisect(arr.slice(i + 1), fn)
    }
    return i
  }

  function bisectAll(data: Schedule, currentTime: Date) {
    const indices = {}
    const fn = (entry: string) => isFuture(entry, currentTime)
    for (const key of keys) {
      indices[key] = bisect(data[key], fn)
    }
    return indices
  }

  $: bisectIndices = bisectAll(data, currentTime)
  
  function scrollCurrentIntoView() {
    const options = {
      inline: "center"
    }
    const key = keys.find((key) => nowElems[key]) // find first key that exists in nowElems
    key && nowElems[key].scrollIntoView(options) // scroll it into view
  }

  let nowElems = {}
  afterUpdate(() => {
    const [x, y] = [window.scrollX, window.scrollY]
    scrollCurrentIntoView()
    window.scrollTo(x, y)
  })
</script>

<div class="table-container">
  <table>
    <tbody>
      {#each keys as key}
        <tr>
          <th>{key}</th>
          {#each data[key] as entry, i}
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

  td,
  th {
    text-align: left;
    padding: 5px 10px;
    margin: 0;
    border: 1px solid grey;
    border-top-width: 0px;
    white-space: nowrap;
  }

  tbody tr {
    border-bottom: 1px solid #dddddd;
  }

  tbody tr:nth-of-type(odd) {
    background-color: #fff;
  }

  tbody tr:nth-of-type(even) {
    background-color: #dadada;
  }

  tr:nth-of-type(even) > .highlight {
    background-color: rgb(138, 202, 132);
  }

  tr:nth-of-type(odd) > .highlight {
    background-color: rgb(138, 202, 132, 0.5);
  }

  /* Minimum width */
  @media (max-width: 35rem) {
    th {
      white-space: normal;
    }
  }


</style>
