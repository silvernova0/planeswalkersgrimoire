<script setup>
</script>

<template>
  <div class="relative flex size-full min-h-screen flex-col bg-[#111714] dark group/design-root overflow-x-hidden" style='font-family: "Spline Sans", "Noto Sans", sans-serif;'>
    <div class="layout-container flex h-full grow flex-col">
      <header class="flex items-center justify-between whitespace-nowrap border-b border-solid border-b-[#29382f] px-10 py-3">
        <div class="flex items-center gap-4 text-white">
          <div class="size-4">
            <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path
                fill-rule="evenodd"
                clip-rule="evenodd"
                d="M39.475 21.6262C40.358 21.4363 40.6863 21.5589 40.7581 21.5934C40.7876 21.655 40.8547 21.857 40.8082 22.3336C40.7408 23.0255 40.4502 24.0046 39.8572 25.2301C38.6799 27.6631 36.5085 30.6631 33.5858 33.5858C30.6631 36.5085 27.6632 38.6799 25.2301 39.8572C24.0046 40.4502 23.0255 40.7407 22.3336 40.8082C21.8571 40.8547 21.6551 40.7875 21.5934 40.7581C21.5589 40.6863 21.4363 40.358 21.6262 39.475C21.8562 38.4054 22.4689 36.9657 23.5038 35.2817C24.7575 33.2417 26.5497 30.9744 28.7621 28.762C30.9744 26.5497 33.2417 24.7574 35.2817 23.5037C36.9657 22.4689 38.4054 21.8562 39.475 21.6262ZM4.41189 29.2403L18.7597 43.5881C19.8813 44.7097 21.4027 44.9179 22.7217 44.7893C24.0585 44.659 25.5148 44.1631 26.9723 43.4579C29.9052 42.0387 33.2618 39.5667 36.4142 36.4142C39.5667 33.2618 42.0387 29.9052 43.4579 26.9723C44.1631 25.5148 44.659 24.0585 44.7893 22.7217C44.9179 21.4027 44.7097 19.8813 43.5881 18.7597L29.2403 4.41187C27.8527 3.02428 25.8765 3.02573 24.2861 3.36776C22.6081 3.72863 20.7334 4.58419 18.8396 5.74801C16.4978 7.18716 13.9881 9.18353 11.5858 11.5858C9.18354 13.988 7.18717 16.4978 5.74802 18.8396C4.58421 20.7334 3.72865 22.6081 3.36778 24.2861C3.02574 25.8765 3.02429 27.8527 4.41189 29.2403Z"
                fill="currentColor"
              ></path>
            </svg>
          </div>
          <h2 class="text-white text-lg font-bold leading-tight tracking-[-0.015em]">Planeswalker's Grimoire</h2>
        </div>
        <div class="flex flex-1 justify-end gap-8">
          <label class="flex flex-col min-w-40 !h-10 max-w-64">
            <div class="flex w-full flex-1 items-stretch rounded-lg h-full">
              <div
                class="text-[#9eb7a8] flex border-none bg-[#29382f] items-center justify-center pl-4 rounded-l-lg border-r-0"
                data-icon="MagnifyingGlass"
                data-size="24px"
                data-weight="regular"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
                  <path
                    d="M229.66,218.34l-50.07-50.06a88.11,88.11,0,1,0-11.31,11.31l50.06,50.07a8,8,0,0,0,11.32-11.32ZM40,112a72,72,0,1,1,72,72A72.08,72.08,0,0,1,40,112Z"
                  ></path>
                </svg>
              </div>
              <input
                placeholder="Search"
                class="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-white focus:outline-0 focus:ring-0 border-none bg-[#29382f] focus:border-none h-full placeholder:text-[#9eb7a8] px-4 rounded-l-none border-l-0 pl-2 text-base font-normal leading-normal"
                value=""
              />
            </div>
          </label>
          <button
            class="flex max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 bg-[#29382f] text-white gap-2 text-sm font-bold leading-normal tracking-[0.015em] min-w-0 px-2.5"
          >
            <div class="text-white" data-icon="Plus" data-size="20px" data-weight="regular">
              <svg xmlns="http://www.w3.org/2000/svg" width="20px" height="20px" fill="currentColor" viewBox="0 0 256 256">
                <path d="M224,128a8,8,0,0,1-8,8H136v80a8,8,0,0,1-16,0V136H40a8,8,0,0,1,0-16h80V40a8,8,0,0,1,16,0v80h80A8,8,0,0,1,224,128Z"></path>
              </svg>
            </div>
          </button>
          <div
            class="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-10"
            style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuDvlbK1NjjBFt4WxcDM5ojTmHXJzT0Pv7tMeCEYTrEYBoj5oy0q3JJq7ZWcY3dm8JhvbyG1VosL1o53aLG9pt_CxsuT-ghikUbpLk12jIC-blutr7lYMCpbkpdCr9bM16tFbCDYW_GcYsWzgN2tZNEtF0ZMuHf3fPrn_E4mJkMBIMp7xTTya0SidgZwvUNhJdWb1py1hiwhoVp15mwUDpNmsREVZsdxUzmHfrOmDFyOjEhwvAo5qqWygfPntENAl4bGvFCLUZ8veQ");'
          ></div>
        </div>
      </header>
      <div class="px-40 flex flex-1 justify-center py-5">
        <div class="layout-content-container flex flex-col max-w-[960px] flex-1">
          <div class="flex flex-wrap justify-between gap-3 p-4"><p class="text-white tracking-light text-[32px] font-bold leading-tight min-w-72">Welcome back, Sarah</p></div>
          <h2 class="text-white text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">Collection Overview</h2>
          <div class="flex flex-wrap gap-4 p-4">
            <div class="flex min-w-[158px] flex-1 flex-col gap-2 rounded-lg p-6 border border-[#3d5245]">
              <p class="text-white text-base font-medium leading-normal">Total Cards</p>
              <p class="text-white tracking-light text-2xl font-bold leading-tight">1,234</p>
            </div>
            <div class="flex min-w-[158px] flex-1 flex-col gap-2 rounded-lg p-6 border border-[#3d5245]">
              <p class="text-white text-base font-medium leading-normal">Total Value</p>
              <p class="text-white tracking-light text-2xl font-bold leading-tight">$5,678</p>
            </div>
            <div class="flex min-w-[158px] flex-1 flex-col gap-2 rounded-lg p-6 border border-[#3d5245]">
              <p class="text-white text-base font-medium leading-normal">Unique Sets</p>
              <p class="text-white tracking-light text-2xl font-bold leading-tight">25</p>
            </div>
          </div>
          <h2 class="text-white text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">Quick Actions</h2>
          <div class="flex justify-stretch">
            <div class="flex flex-1 gap-3 flex-wrap px-4 py-3 justify-between">
              <button
                class="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-[#38e07b] text-[#111714] text-sm font-bold leading-normal tracking-[0.015em]"
              >
                <span class="truncate">Add Cards</span>
              </button>
              <button
                class="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-[#29382f] text-white text-sm font-bold leading-normal tracking-[0.015em]"
              >
                <span class="truncate">View Collection</span>
              </button>
            </div>
          </div>
          <h2 class="text-white text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">Recent Additions</h2>
          <div class="grid grid-cols-[repeat(auto-fit,minmax(158px,1fr))] gap-3 p-4">
            <div class="flex flex-col gap-3">
              <div
                class="w-full bg-center bg-no-repeat aspect-square bg-cover rounded-lg"
                style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuACBHj0vNIZjKPeyxz0Hbjr06AtVucPuDHp_TJY-c7U2Rd3RteYMb7M0VgVlaC7nHPQrqb_enRwn2HOUnP2gaAJna8qZB8qbcJeQmzWgMnSpfh1BUeWObQRKlXwALvYdGZzDX6Z0Hzlz5ASL1-DYRsAfNai0m8EDBCzGgmlCVlcKrWJ5ElQzF4GNpkn215XNe9eQN6XSF_6adoXWTb9nlFsADmFDO4hpXtkZp4Pu9vwX2zTHkRvvT79xG3XHDCnn7wEw-zzyqsF_g");'
              ></div>
            </div>
            <div class="flex flex-col gap-3">
              <div
                class="w-full bg-center bg-no-repeat aspect-square bg-cover rounded-lg"
                style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuDEp4x_2mYOq_GyBDuYoTkca-W4_aw-hrr4thUne-feN0HHsXYfhudIErzMXE9vQ82RSojhr83FkenN0nm8nB-U4AnytHxXxrJQbA4oQQ1LTWkpug9gjfMgZS9ijn6NYXk-qrmeBnJ_gNGfsBEJeFLjRQGqNJ5VMjW5gInTH5IXuuc1zM31gbv9XrprfBJgsjFf7MB7iiIs3Rvik-Yp-Z8xUMmDcxs84WqnwCUQauif1A2HVp_uGjMhxhuo6joVwoa5m7FQt01kRg");'
              ></div>
            </div>
            <div class="flex flex-col gap-3">
              <div
                class="w-full bg-center bg-no-repeat aspect-square bg-cover rounded-lg"
                style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuCZE4Di7wS4UDk53178IH3SDRLzFVVXlHHEod-NR9KsuCWOoxoPDfk6t5vm8ffKXfSXQKzxfQZyWrXSmzQippTXPSGsqq0oOoE6PEq05wnbPqIR1EvXMK2Eq0mpv5j8vDctSuuF4E16-qRPUAAwDtD7-DaMzZTj-Zg28zv-J03egtpcnuHA2GLHNWuN4vVd0BHarxuhZjvxces36ySjrv1PlmeMpppeXRDQcu7UztiU5FudW52RTX_pxZ6YNP-NjT_1hinN3H3edQ");'
              ></div>
            </div>
            <div class="flex flex-col gap-3">
              <div
                class="w-full bg-center bg-no-repeat aspect-square bg-cover rounded-lg"
                style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuBI6emHyt3ggyP5Oyxrd0obVToMuvgOYTvRv2tPsTFbfPa7zlaupbY8c5i2zYgUeVoi4vdz7xSAqr99-7PzVwDqIXE2ORnUFCJbaILgB3iMmhkt4yz6OG4BeNyod6I_MRVTRFO35D_InWEVwUgIpXtL0Oon-VyfR3uVFNKPyvRuDTOBnKl6uoo0GYkY6O_rSjWlKumOUe9BivADmtKfR3q8kah-dvWs3213PQf3R8H4vi1uqlFnaB9ycbq9XwoE6kK-IEeO1TLo6w");'
              ></div>
            </div>
          </div>
          <h2 class="text-white text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">Popular Sets</h2>
          <div class="flex overflow-y-auto [-ms-scrollbar-style:none] [scrollbar-width:none] [&amp;::-webkit-scrollbar]:hidden">
            <div class="flex items-stretch p-4 gap-3">
              <div class="flex h-full flex-1 flex-col gap-4 rounded-lg min-w-40">
                <div
                  class="w-full bg-center bg-no-repeat aspect-square bg-cover rounded-lg flex flex-col"
                  style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuBJfWKCYi8cPsHI6D9uqMSjLPlzY7gejftJVjWvLu5fp7B5SOWGE9EW8nXIj4HUk4kdf9KYZk1MPMNqB-jihx-iRfxMxq0xoh9NHzXBG1xJmYATc7TJgBmA_RXhqY0oHUesDWRHlDd12yCs9-OxLiRgocwdxjT3OJae0-Yw_IiZi87-4Jlk3abllbhaer-aUn0VMrWqBIbMvOkWbkMVDheKaCvrn5alXm4wqwss0B5OoNPjMVWKuOtfqwtWfd9GdbTRUH553mHmmw");'
                ></div>
                <p class="text-white text-base font-medium leading-normal">Dominaria United</p>
              </div>
              <div class="flex h-full flex-1 flex-col gap-4 rounded-lg min-w-40">
                <div
                  class="w-full bg-center bg-no-repeat aspect-square bg-cover rounded-lg flex flex-col"
                  style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuAA75Jf3G38tHXFJyJoQQ_kYBPlcwENhDcVAy9qg7-n-pQwuVjYrRb8TCL0FfPex5Vlcie18iR5YYsCLZbaanyhQ6U-ohpYTwyO4Fsu87wZtGSek3gSoTRwVWGvTtB05MOR66Pyls7bR9Tt5ogg07CWtEQl9z4BDkTffXk9HxvhlVw7NbGz8ufcRvmEDc3D5azg3N_cJUUaOBCXSOo981TQmHocide3dz_pF7XcqK9SGAzPxfBRfViVh4f0aBw8jUmEbpz3SGnJJw");'
                ></div>
                <p class="text-white text-base font-medium leading-normal">Innistrad: Crimson Vow</p>
              </div>
              <div class="flex h-full flex-1 flex-col gap-4 rounded-lg min-w-40">
                <div
                  class="w-full bg-center bg-no-repeat aspect-square bg-cover rounded-lg flex flex-col"
                  style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuC8NVmC7IqCjk2AIseTc8EoC3jnhHTQvJuJ6bbWSv8jNS8mq9Wl4L1TcWnnhex5Tc9ISe4pi9FxHHgjzPQdCNPiJ9qIgRxbNh95sek6jvXqA8vuaWb2Jn6sGen2Hb7DQw8-UD6tlfVMqmkpiVTWC_VcjmBhQjKB5Bo4aJU6ZutpQ52VpgnZ4ZyhJGMDrtrG_P_06AP1aa4yYBIQio44mhtMDaRRgIBElKiz4sQ9_-sx_LqybPazVqW58MGEEemViYUCEVvtzuRDSQ");'
                ></div>
                <p class="text-white text-base font-medium leading-normal">Strixhaven: School of Mages</p>
              </div>
              <div class="flex h-full flex-1 flex-col gap-4 rounded-lg min-w-40">
                <div
                  class="w-full bg-center bg-no-repeat aspect-square bg-cover rounded-lg flex flex-col"
                  style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuBrq1_boHXjcPzobn4Bsiy2KDLyMAK3wdo9eXTnmoKK283DksJ9ENnhszrYXo9VAT2rtxh-Rx8xnB5_Mlms9T0YJfdlsKaq0umlgafPrvfnpJjf94kitfYnlr_Tob26COYUzw8bkgLYniLztVD9ZWKrJQFQRWfcx91EGjyx2UM9hBfa5e0O3wroekRpR6z81qfr9VEGiMoTkFe6o5d-UJLa185RWaKK2yv2a405Cp5l5pAhFh5E3xhER8rmgqTqx8d86cXuftuJMQ");'
                ></div>
                <p class="text-white text-base font-medium leading-normal">Kaldheim</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>