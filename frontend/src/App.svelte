<script lang="ts">
  import { onMount } from 'svelte'

  import Table from './Table.svelte'

  export let apiUrl: string

  let schedules: Object = {}
  let now = new Date()
  onMount(() => {
    const interval = setInterval(() => {
      now = new Date()
    }, 1000)
  })

  $: isWeekend = now.getDay() === 6 || now.getDay() === 0
  $: suffix = isWeekend ? 'Weekend' : 'Weekday'

  $: scheduleNames = Object.keys(schedules).filter((name) =>
    name.endsWith(suffix)
  )

  fetch(apiUrl)
    .then((resp) => resp.json())
    .then((res) => {
      schedules = res
    })
    .catch((err) => console.log(err))
</script>

<main>
  <a href="https://parking.wustl.edu/campus-shuttle-system/">
    <h2>WashU Shuttles</h2>
  </a>

  <p>
    A sane alternative to Washington University in St. Louis Parking &
    Transportation's shuttle schedule website.
  </p>

  <section>
    {#if !schedules}
      <p>Waiting for data to load...</p>
    {:else}
      <p>{now}</p>
      {#each scheduleNames as name}
        <a
          href={'src_url' in schedules[name]
            ? schedules[name]['src_url']
            : './'}
        >
          <h3>
            {name}
          </h3>
        </a>
        <Table data={schedules[name]} currentTime={now} />
      {/each}
    {/if}
  </section>

  <br />

  <footer>
    <p>
      Data built from
      <a href="https://parking.wustl.edu/campus-shuttle-system/">
        <span>WashU Parking & Transportation</span>
      </a>
      and
      <a href="https://www.metrostlouis.org/">
        <span>Metro STL</span>
      </a>
      .
    </p>

    <p>
      This site is the result of my frustration with WashU Parking &
      Transportation's website and my attempt at a more accessible bus schedule
      table for myself. If anything is not accurate or if you have any
      suggestions for improvement, please email me at tnie at wustl dot edu.
      Source code hosted on Github:
      <a href="https://github.com/kwsp/washu-shuttles/">
        https://github.com/kwsp/washu-shuttles/
      </a>
    </p>
  </footer>
</main>

<style>
  main {
    text-align: center;
    padding: 1em;
    /* max-width: 240px; */
    margin: 0 auto;
  }

  h2 {
    color: #ff3e00;
    text-transform: uppercase;
    font-weight: 300;
  }

  a {
    text-decoration: underline;
    color: inherit;
  }

  @media (min-width: 640px) {
    main {
      max-width: none;
    }
  }
</style>
