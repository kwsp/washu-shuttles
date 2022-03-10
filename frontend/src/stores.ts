import { readable } from 'svelte/store'

export const time = readable(new Date(), function start(set) {
  const interval = setInterval(() => {
    set(new Date())
  }, 10000)

  return function stop() {
    clearInterval(interval)
  }
})

const apiUrl = './data.json'

export const schedules = readable(
  {
    shuttleNames: [],
    buildDate: '',
  },
  (set) => {
    fetch(apiUrl)
      .then((resp) => resp.json())
      .then(set)
      .catch((err) => console.log(err))
    return () => {}
  }
)
