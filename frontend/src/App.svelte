<script lang="ts">
  import { afterUpdate } from 'svelte'
  import { time, schedules } from './stores'
  import Schedule from './Schedule.svelte'

  const dateOptions = {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: 'numeric',
    minute: 'numeric',
  } as const

  afterUpdate(() => {
    window.scrollTo(0, 0)
  })
</script>

<main>
  <a href="./"><h2>WashU Shuttles</h2></a>
  <p>Current time: {$time.toLocaleDateString('en-US', dateOptions)}</p>

  <section>
    {#each $schedules.shuttleNames as name}
      <Schedule {name} schedule={$schedules[name]} />
    {/each}
  </section>

  <br />
  <section>
    <p>
      This site is my attempt at a more accessible shuttle schedule page than
      WashU Parking & Transportation's website. If anything is not accurate or
      if you have any suggestions for improvement, please email me at tnie at
      wustl dot edu. Source code hosted on Github:
      <a href="https://github.com/kwsp/washu-shuttles/">
        https://github.com/kwsp/washu-shuttles/
      </a>
    </p>
  </section>

  <footer>
    <p>
      Data built from
      <a href="https://parking.wustl.edu/campus-shuttle-system/">
        WashU Parking & Transportation
      </a>
      and
      <a href="https://www.metrostlouis.org/">Metro STL</a>
      on {$schedules.buildDate}.
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
