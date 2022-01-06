<script lang="ts">
  export let data: JSON
  export let currentTime: Date

  interface Schedule {
    [stop: string]: Array<string | null>
  }

  // if ordered keys provided, use that
  const keys: Array<string> = data['keys'] || Object.keys(data)

  function parseTime(s: string): Date {
    const res = s.match(/(1[0-2]|0?[1-9]):([0-5][0-9]) ?([AaPp][Mm])/)

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

  function transformSchedule(data) {
    return data
  }

  const schedule: Schedule = transformSchedule(data)

  // Predicate to check if this bus will arrive in the future
  function isFuture(entry: string | null): Boolean {
    return entry != null && currentTime < parseTime(entry)
  }

  // get CSS class based on time to determine highlight
  function getClass(entry: string): string {
    return entry && isFuture(entry) ? 'highlight' : ''
  }
</script>

<div class="table-container">
  <table>
    <tbody>
      {#each keys as key}
        <tr>
          <th class="fixed">{key}</th>
          {#each schedule[key] as entry, i}
            <td class={getClass(entry)}>
              {entry}
            </td>
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
