<script lang="ts">
  export let data: JSON

  interface Entry {
    time: Date
    str: string
    ampm: string
  }

  interface Schedule {
    [stop: string]: Array<Entry | null>
  }

  // if ordered keys provided, use that
  const keys: Array<string> = data['keys'] || Object.keys(data)
  const ampm: Array<string> = data[keys[0]].map(
    (entry) => entry.match(/[AaPp][Mm]/)[0]
  )

  const currentTime = new Date()

  function transformEntry(s: string | null): Entry | null {
    if (!s) {
      return null
    }
    const res = s.match(/(1[0-2]|0?[1-9]):([0-5][0-9]) ?([AaPp][Mm])/)
    try {
      const hour = parseInt(res[1])
      const minute = parseInt(res[2])
      const ampm = res[3]

      const d = new Date()
      d.setHours(ampm.match(/[Pp][Mm]/) ? (hour % 12) + 12 : hour)
      d.setMinutes(minute)
      return {
        time: d,
        str:
          hour.toString().padStart(2, '0') +
          ':' +
          minute.toString().padStart(2, '0'),
        ampm: ampm,
      }
    } catch (err) {}
  }

  function transformSchedule(data) {
    let obj = {}
    for (const key of keys) {
      obj[key] = data[key].map((s) => transformEntry(s))
    }
    return obj
  }

  const schedule: Schedule = transformSchedule(data)

  // Predicate to check if this bus will arrive in the future
  const isFuture = (entry: Entry | null): Boolean => {
    if (!entry) {
      return false
    }
    return currentTime < entry.time
  }
</script>

<div class="table-container">
  <table>
    <thead>
      <tr>
        <th />
        {#each ampm as val}
          <th>{val}</th>
        {/each}
      </tr>
    </thead>

    <tbody>
      {#each keys as key}
        <tr>
          <th class="fixed">{key}</th>
          {#each data[keys[0]] as _, i}
            <td
              class={schedule[key][i] && isFuture(schedule[key][i])
                ? 'highlight'
                : ''}
              >{schedule[key][i] ? schedule[key][i].str : ''}
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
