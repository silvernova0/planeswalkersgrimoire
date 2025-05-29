<script setup>
</script>

<template>
  <div class="relative flex size-full min-h-screen flex-col bg-[#111714] dark group/design-root overflow-x-hidden" style='font-family: "Spline Sans", "Noto Sans", sans-serif;'>
    <div class="layout-container flex h-full grow flex-col">
      <header class="flex items-center justify-between whitespace-nowrap border-b border-solid border-b-[#29382f] px-10 py-3">
        <div class="flex items-center gap-8">
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
          <div class="flex items-center gap-9">
            <a class="text-white text-sm font-medium leading-normal" href="#">Home</a>
            <a class="text-white text-sm font-medium leading-normal" href="#">Sets</a>
            <a class="text-white text-sm font-medium leading-normal" href="#">Decks</a>
            <a class="text-white text-sm font-medium leading-normal" href="#">Collection</a>
            <a class="text-white text-sm font-medium leading-normal" href="#">Wishlist</a>
          </div>
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
            <div class="text-white" data-icon="Bell" data-size="20px" data-weight="regular">
              <svg xmlns="http://www.w3.org/2000/svg" width="20px" height="20px" fill="currentColor" viewBox="0 0 256 256">
                <path
                  d="M221.8,175.94C216.25,166.38,208,139.33,208,104a80,80,0,1,0-160,0c0,35.34-8.26,62.38-13.81,71.94A16,16,0,0,0,48,200H88.81a40,40,0,0,0,78.38,0H208a16,16,0,0,0,13.8-24.06ZM128,216a24,24,0,0,1-22.62-16h45.24A24,24,0,0,1,128,216ZM48,184c7.7-13.24,16-43.92,16-80a64,64,0,1,1,128,0c0,36.05,8.28,66.73,16,80Z"
                ></path>
              </svg>
            </div>
          </button>
          <div
            class="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-10"
            style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuD0uWy4lh4bshRRkuBJq1x6Q000QbAvKRyw1gKzFqL9Ch06WkorGPnksPZAQ-UIN0vKee2s03XfxtkyGFIMxvo7qwOZnBW8CPRLv46sRckzkSdJ9zzYrqGaaWeT_TZL5YwP9U2OKlA8l_9EGp3JGRxETMVNsAgY_z3M1Mb6ceg4ad0JwjhEsRkR-lAaYAe8OFnkZBgl8Tj9QE6N5VScMMEfOkhh3yThvZk5dADBzYPA0Qd6wVhTySBpQc-ooMog769j3CpE9palRg");'
          ></div>
        </div>
      </header>
      <div class="px-40 flex flex-1 justify-center py-5">
        <div class="layout-content-container flex flex-col max-w-[960px] flex-1">
          <div class="flex flex-wrap justify-between gap-3 p-4">
            <div class="flex min-w-72 flex-col gap-3">
              <p class="text-white tracking-light text-[32px] font-bold leading-tight">Collection</p>
              <p class="text-[#9eb7a8] text-sm font-normal leading-normal">1,234 cards</p>
            </div>
          </div>
          <div class="px-4 py-3">
            <label class="flex flex-col min-w-40 h-12 w-full">
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
                  placeholder="Search for cards"
                  class="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-white focus:outline-0 focus:ring-0 border-none bg-[#29382f] focus:border-none h-full placeholder:text-[#9eb7a8] px-4 rounded-l-none border-l-0 pl-2 text-base font-normal leading-normal"
                  value=""
                />
              </div>
            </label>
          </div>
          <div class="flex gap-3 p-3 flex-wrap pr-4">
            <button class="flex h-8 shrink-0 items-center justify-center gap-x-2 rounded-lg bg-[#29382f] pl-4 pr-2">
              <p class="text-white text-sm font-medium leading-normal">Color</p>
              <div class="text-white" data-icon="CaretDown" data-size="20px" data-weight="regular">
                <svg xmlns="http://www.w3.org/2000/svg" width="20px" height="20px" fill="currentColor" viewBox="0 0 256 256">
                  <path d="M213.66,101.66l-80,80a8,8,0,0,1-11.32,0l-80-80A8,8,0,0,1,53.66,90.34L128,164.69l74.34-74.35a8,8,0,0,1,11.32,11.32Z"></path>
                </svg>
              </div>
            </button>
            <button class="flex h-8 shrink-0 items-center justify-center gap-x-2 rounded-lg bg-[#29382f] pl-4 pr-2">
              <p class="text-white text-sm font-medium leading-normal">Rarity</p>
              <div class="text-white" data-icon="CaretDown" data-size="20px" data-weight="regular">
                <svg xmlns="http://www.w3.org/2000/svg" width="20px" height="20px" fill="currentColor" viewBox="0 0 256 256">
                  <path d="M213.66,101.66l-80,80a8,8,0,0,1-11.32,0l-80-80A8,8,0,0,1,53.66,90.34L128,164.69l74.34-74.35a8,8,0,0,1,11.32,11.32Z"></path>
                </svg>
              </div>
            </button>
            <button class="flex h-8 shrink-0 items-center justify-center gap-x-2 rounded-lg bg-[#29382f] pl-4 pr-2">
              <p class="text-white text-sm font-medium leading-normal">Set</p>
              <div class="text-white" data-icon="CaretDown" data-size="20px" data-weight="regular">
                <svg xmlns="http://www.w3.org/2000/svg" width="20px" height="20px" fill="currentColor" viewBox="0 0 256 256">
                  <path d="M213.66,101.66l-80,80a8,8,0,0,1-11.32,0l-80-80A8,8,0,0,1,53.66,90.34L128,164.69l74.34-74.35a8,8,0,0,1,11.32,11.32Z"></path>
                </svg>
              </div>
            </button>
            <button class="flex h-8 shrink-0 items-center justify-center gap-x-2 rounded-lg bg-[#29382f] pl-4 pr-2">
              <p class="text-white text-sm font-medium leading-normal">Type</p>
              <div class="text-white" data-icon="CaretDown" data-size="20px" data-weight="regular">
                <svg xmlns="http://www.w3.org/2000/svg" width="20px" height="20px" fill="currentColor" viewBox="0 0 256 256">
                  <path d="M213.66,101.66l-80,80a8,8,0,0,1-11.32,0l-80-80A8,8,0,0,1,53.66,90.34L128,164.69l74.34-74.35a8,8,0,0,1,11.32,11.32Z"></path>
                </svg>
              </div>
            </button>
            <button class="flex h-8 shrink-0 items-center justify-center gap-x-2 rounded-lg bg-[#29382f] pl-4 pr-2">
              <p class="text-white text-sm font-medium leading-normal">Format</p>
              <div class="text-white" data-icon="CaretDown" data-size="20px" data-weight="regular">
                <svg xmlns="http://www.w3.org/2000/svg" width="20px" height="20px" fill="currentColor" viewBox="0 0 256 256">
                  <path d="M213.66,101.66l-80,80a8,8,0,0,1-11.32,0l-80-80A8,8,0,0,1,53.66,90.34L128,164.69l74.34-74.35a8,8,0,0,1,11.32,11.32Z"></path>
                </svg>
              </div>
            </button>
          </div>
          <div class="grid grid-cols-[repeat(auto-fit,minmax(158px,1fr))] gap-3 p-4">
            <div class="flex flex-col gap-3">
              <div
                class="w-full bg-center bg-no-repeat aspect-[3/4] bg-cover rounded-lg"
                style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuBfN0i3j1PvqYMjwF1V-meXjI-kN_PKGBFVBaRSDSLAPW6JyHswWaWw82s0O7Xox56JswLXgWGsT1iCGJamNlnVbqEc7YVVsE68JDvSu2lQ7WCYwD5FYqpbJMBk-DflZlFN1x7f348YSQlh7pLiQie0ieW1-c7Ii3Z2Y2tSfr8a3xvx8TzoiMVUf6qe5j4YcMDuvlKME4PBqMOw_7QRUedwrdYb1QyfKDrIlkL-L-Kq-Sv_q87RH6qJipiUtYf2ypKvwszDwPD9fw");'
              ></div>
            </div>
            <div class="flex flex-col gap-3">
              <div
                class="w-full bg-center bg-no-repeat aspect-[3/4] bg-cover rounded-lg"
                style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuAvezxKbJ-kdLK3Zm-A4ZScprIOcV78FeK_PHIlXYYTpUwXAqX3EuU50ZlaxfpOWJIsBKXdfiejEYGc7Iu4ExpJ29Mzd8YUM81vV2_J7sNLzmpPahsI7RAf8VnLqGy3IS6UMdN9EaAuph5f2qLjz_XT6G78YMVNluxUiOesGaNBlCXxvrrqAQ3xEg7Z3W4NlAPNckQCtpGHmttTtVM_ajYuZsw9473JQo8h3oHmYtXF6szghsW0cslB7qC6yBDeUXh8cTIRgRpAlA");'
              ></div>
            </div>
            <div class="flex flex-col gap-3">
              <div
                class="w-full bg-center bg-no-repeat aspect-[3/4] bg-cover rounded-lg"
                style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuA1aYcYidQZ0SyUyUptiahRArtybC8uiMFghQRZOJb9-3jrYb-s2L6ld5sqXHqBFo1vLvVjZ8OosMXrrt7pkh08nb332EGDrpz1ZOyfJinnNk_qiNWG6oN5E5h5ge0P2_vGNW7C2UoXIofpy1_O7ucA1t9o8m337xBIoFPX5JFLiz78RUWLZYioIZruW0XGY3RVIS9rpj0MqwDe2zFuAFpvYTYWW0DXq3hiUynigxubo70OjVje-WZ8uwzmdBhmVk3NMhdKitehRw");'
              ></div>
            </div>
            <div class="flex flex-col gap-3">
              <div
                class="w-full bg-center bg-no-repeat aspect-[3/4] bg-cover rounded-lg"
                style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuD6t74VJxlgqF8tktzl-6TCTzFUHzR9qepwfceLHawcr98s2a7dB977BT9MpdBM__t0JM7DiqXu6gbMd4ug18rKYX_z2sb0lRDk__sUQN0MdjexPBJyUZGCt_y8JAQzdmsLBujoI0XFg6ugp3-1yy6bH4r-aKY7tmT3nr6eMh4TmyMB1KCz1F_9s3eoDTx7N_MlvgQY9uPP4QuQSVDObQHpmeX8LLptFK7VibT0BmYagprz2oxx2VrmjQ3at7M125qPGb69VnHByg");'
              ></div>
            </div>
            <div class="flex flex-col gap-3">
              <div
                class="w-full bg-center bg-no-repeat aspect-[3/4] bg-cover rounded-lg"
                style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuDASkgFgJFVrELDwcjoLehpS-Zkdf9qEgP5mluha2ww4RadFjdiwLJFiMjREzLJ52RmfoFzgGLTUpEkUDXByJPRQ_aB3Qtiw-BTib-ReSi328pa2aLgJyoS44ZTZTHtaam3sQ-j0eKb3cJTDGWMrfY8oBlwJSXkUUhrUnbc7q4DVvmcuVQLDsvuv8ePhnS7kwEeZiqDsPB3QEHXWFmgDeyoC55XDG2sYf4mZlRsdjaH5NNEDG_LCbcA2QbEdieLSX1xSmFIWPLV6A");'
              ></div>
            </div>
            <div class="flex flex-col gap-3">
              <div
                class="w-full bg-center bg-no-repeat aspect-[3/4] bg-cover rounded-lg"
                style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuAGAhEVwnAhqxI2qA1NKUWjl6LTuK2itrRWTUEu0HSLewsiH9GSmcDQ8Xq9zhNG0jImsTawR1LRVsJt2uHYAUdoWGuSxNba1JrglTSoxZY-CFCGLaGvjKVcHPP-bZF2OZ6KgxJZDR1_h3GVEDHtTZ4IqMIBxo-KuGNOd28TOMOsVEfZNNovDi1edok082d4bWss7DIW-nehFn1SyQXD3WH_DjemaPkIdA_Dq_A__RV2Slny3artnJNdXXKIKtawRzqo_xTwEUSm-w");'
              ></div>
            </div>
            <div class="flex flex-col gap-3">
              <div
                class="w-full bg-center bg-no-repeat aspect-[3/4] bg-cover rounded-lg"
                style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuD5qKCk3Eag2VIrvpbxD2ETu589lDlwGeHhKRP8rMBAvXI2nS_t3n5bUa8LVrQJHEP5kOzvVc9rs_9nzJEHcnM3gX2fAIS0IraHvHRajm64mTcbeJD4Jl8FLYJMtQBv_tVLb70--me-jvCofx0tamnYKTG4_dAh5OHP2-uENtEdJjtR9KkAr8RSOHiSb8jhchgukLUv9GdcAdLWOCtJbcEvIkiMetPJjoW1gEuxGgb3v4RhZlUL5oZhdHNEENFUU8OWIFX2CnPCNw");'
              ></div>
            </div>
            <div class="flex flex-col gap-3">
              <div
                class="w-full bg-center bg-no-repeat aspect-[3/4] bg-cover rounded-lg"
                style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuC9L-vA_8A8NvxWdoBiR-t-JNGo3qhCIUE8-opbw4NfY0y7HyAv0TYk_oLBJTy4crn269fXWttteQtM-QN2UaL20rKSNDFmiaehyw8gCaEFnJUhnllvsT363nXWCkv6YTH9F8oi8XyH80l-rL5fNqkeKFyHpca5lPOW0aB8ACaudbBz8QVeDo_9Bq9YvD4CPNqov8n0Al_7cDY0KqjH8Sts15D2lfacUCMaTkgJdBR_MXWj0aAYK2xbeEOJLL74LN23_yqgZGetWw");'
              ></div>
            </div>
            <div class="flex flex-col gap-3">
              <div
                class="w-full bg-center bg-no-repeat aspect-[3/4] bg-cover rounded-lg"
                style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuD2XcK3oaR218i4KjVpuSCScoJyw2LDVtKipV8y1CRegDKKPqf1IsTvq15mDYBDRDV4I0n5TP69G_4bNhpFS0Vh2p7JrKCwdFwGTOaDEGHH-GzEC7n0Vd6vB8mbupXVc_s3KIDHldfruvfdEWh3oEo_3x-A6KCDbmPiC7SK064naa2LUOcUI2oi0dJ0AlSPSFsSU4EUKYEz968p-QiyGQfjlyQwqt65EuYQgaiQYT9qrD5cPMBrqQiH4IOPiW4U6aZqoD0Xjgw1pA");'
              ></div>
            </div>
            <div class="flex flex-col gap-3">
              <div
                class="w-full bg-center bg-no-repeat aspect-[3/4] bg-cover rounded-lg"
                style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuBc067VU1tiesGpt7OvY2j4QHQF0Y4QBejnOmVaOswpUrauo2JTudq6MaZUVwUTRxbpG1RFHoMLfcEwPeWt1lnYysx4Zbnuba8qQ7nm1scRJrPRoXfY2E4ujWJI5J9yDI1jFMor3m8rV3Q5r5uq14pRxjrrOnDyNNpZQYRreWqc_YOSW1exIOL9lYmPOuGdhZ7PkSs9WXQT4XvxmdAzJoxHVNA0rC8kRAcMAI6Se69bblGZbmx19uNSn0MqwWbVSP5I00QrKfhY6Q");'
              ></div>
            </div>
            <div class="flex flex-col gap-3">
              <div
                class="w-full bg-center bg-no-repeat aspect-[3/4] bg-cover rounded-lg"
                style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuBUUhp9FpUgS3MubDY5QlMw6h5OFNBXOl9L7e8XRzaiC-6xTfaT4mQn10NIY4VzwDErZ6AcMGsdd_1IQl5Yyy7x-lImyaXLXiNpPVIyBxZW44GPBL8FsupoZzktsyEEHiaX_ylsoztlj24vdYv5O1yuFD2kgoUvl86v9Xpr3k5rzlVl8eeHr6J2B8PUV_Adk4X39ePLsf-GQAp6WVvttp0k9pbHPOyOBh62_YUvDc1fDyw2nIyxQFytOYRbBK1YZbUjlRvzkLt0nw");'
              ></div>
            </div>
            <div class="flex flex-col gap-3">
              <div
                class="w-full bg-center bg-no-repeat aspect-[3/4] bg-cover rounded-lg"
                style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuDSqznHdvgnWsDIuZ3aG4K67T18FpRUvJpZ8U4Fs_8cOWjaWDtFOl4iexeo7gnclFRZdbQ8e40HBeEP0FVz54JnWVpp-DUs_UZAbokqpfO5ndeEy3eGJjMVNz3htz_rw8KQ1VTdMqYrrWuNe-qWfZBd2rvuZk0piHSp0QxZTvUj8TWh1vcTg3i0WD8FPbjqDQRYn1nRU75BWvVCX2saEX00IKiccf9ynFtWUwO23RE6vNTXmOAvb8BtQmCRYgAjsVNYcAyoIjf0Tw");'
              ></div>
            </div>
            <div class="flex flex-col gap-3">
              <div
                class="w-full bg-center bg-no-repeat aspect-[3/4] bg-cover rounded-lg"
                style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuCPdxu6oK0ilB00YfWY3Xp7cygB1VvK1qumfWz4RPz9W4IJ698mdERw9UNc7UrdfSp-gevxAU30kMeUUd2X-X2WJ8x2mpyTRpwiHucxsMPe2P9_habMyvgb3yAyqrjg9O9_tlu_CMVtJDDWC6tQNT3FzjTJTTk5-xNGBs6O_ZZ1wMnWfkT-ixh8o5yxYnt7K4pguEM4SafFVNqbkccbbs_zdaPP4fmFSyzTBHrceFiXOeUrK2DyDT8q5tnPY_MDW5kpRr2FTUNwZw");'
              ></div>
            </div>
            <div class="flex flex-col gap-3">
              <div
                class="w-full bg-center bg-no-repeat aspect-[3/4] bg-cover rounded-lg"
                style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuA_YFdlald4p7rIGxK6ss1kfhhOpxdf1z7cqOQRCVJAJUDhXGeb5YCCgVq_pb0Xvthg7UQOd3RWo4eHPwpCf56DPSuySyKMhjpID62dxFpMW9OOtwi2bMpUEpy2QFC4Ny9yT9fItsE0kgzuflfBTTooRKF8GK9bOBEmyKEwZHe4xP5XBq9K4YGixvDCxOZRVRfh7_CNWnFe8pJF0hJ1zKlyG4NysZhFmZa-HVZk_3NdaXpFjBBZW7CSmqUo5-w65SzFN7NMGclL0Q");'
              ></div>
            </div>
            <div class="flex flex-col gap-3">
              <div
                class="w-full bg-center bg-no-repeat aspect-[3/4] bg-cover rounded-lg"
                style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuDT83Wt6razYrRx5bLJAIrPaIzIs954n9HD-INOyWG30lIyMOAZbDIaPuYMcNo3LD_UjrgRKKLTpzdq4vuJqBTJTYVk_6XWJ2vwYUuwAToGhFGx4WDzTZb-f9d2Dxw5zpgYFczRImCqvc21HO7zhyz0mV7AcNPzfbl_j9Ka9QL6AUcxTqAdL-4lD0FoI6ku_SV9gV_ekkwa2Kb6RhYAhv_IitSyUz0rlsPp9H2OkXlvZSyq7ydRJXmCG4e2JeKZs5h_dH2uOWiqcg");'
              ></div>
            </div>
            <div class="flex flex-col gap-3">
              <div
                class="w-full bg-center bg-no-repeat aspect-[3/4] bg-cover rounded-lg"
                style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuB56tWnV7gJbgA6PCwl9phyau7CKt3hS620oz-zloDatn-gj2zuP2nhC8fdj5D9z-ZSfAMLCXlxew9Qz4lT0F21VM_jJ3q2CMWMxz7Z1Dui4KC9DxEmFJ5qr5xyvZNC7AcP93-NYk2lGRBDgaGcP7VjvB7_oe4b7BnMLdbkhTNRWjrpe489OIjStZFlYjfP2nOL5brMsxZsSrhcOMLNaNwI-N2yMRLMaCXx0vAJSPJeeUuCIumSSRr7bikBx-rTZFSyI3IYVthKGA");'
              ></div>
            </div>
            <div class="flex flex-col gap-3">
              <div
                class="w-full bg-center bg-no-repeat aspect-[3/4] bg-cover rounded-lg"
                style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuD91GlBFEp5Xlj85RMrxBQRqAe0M6VfJ9-JEc4BPxDgPrCDFPX6Xrd05ZtwzJOanOBP84IaLl7c4DwqJKDnH4WUdrOXSIsWY99Ob_E_C1Gwhe6gAidswkOgk6T-UoMZ_YT3W4IQcS9bhAmNcnTh3OgpG-3vXsxxzNj45KlmjEKC_yyVgTcVq21wrxwd1f315LS6nlIP2PtrIZPAqG7KMCyYBqknlGCygzC8HonpUKHEDiTsryaeR5a7X9nAC3pCH6AgCx72KfmUtw");'
              ></div>
            </div>
            <div class="flex flex-col gap-3">
              <div
                class="w-full bg-center bg-no-repeat aspect-[3/4] bg-cover rounded-lg"
                style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuDbtK8w9Fep8ICgKvNy7apRcsav6IaU5Cu-6Ut0V-X0Dh-LfhUk_d7Ud6QBOmJpr6uR9rruI6Em19z8qpCDTdqqrxm98qajsq94OrSQwzpvKVaKZACSoGcvAHt2qvH7MLegZzW8hUJ1C_G61O2jdZZcCEGtUa9PIf7DzOGiMLMUNDw6DXjXS3fusl4yP_hKU9QX6DpWwO7eacMbChdiedwPRYZbU9isJSSWFUvf3O1AfnXN8ExS1vV0IRUkvMw2JJ5JPOHsaqNq8w");'
              ></div>
            </div>
            <div class="flex flex-col gap-3">
              <div
                class="w-full bg-center bg-no-repeat aspect-[3/4] bg-cover rounded-lg"
                style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuAS4gOQgJgXcgYOAlVAGA2NUyAXYEXTAd0WqOaviqeRZwa6mZwEdp-drPsgfmaF3CNmzdXP6uPV71tke2n3AEfPiYUuQ7rs-r4RpZh_qkMm6xzwSakrRfVacdWYMcKTilqmKPn8SAMx4-xqPK7VIoK2qIkapKMH6dg0l6cYSqQUyxia4pyztPC26u7WbpKniAeJot1AD5Q8_IwGzPIXqXw2AF6X2fbadtFfKjzBb8IqXKf0-fwYm6i5DK9SQnS2WeB0KaI9N2kFfw");'
              ></div>
            </div>
            <div class="flex flex-col gap-3">
              <div
                class="w-full bg-center bg-no-repeat aspect-[3/4] bg-cover rounded-lg"
                style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuCd9TxY07Twd-msNejyS6wS2cilK-iP8LDgE19Nd2SzYAyN0AnrDt8CyUPDGe3DUN2j7UxYN4_fBEVhFEwH5GunAXbKVVSxVLKX4NxXEyyB_8sH94GAsBZQFnwVDfM9Q9mOa3_ABuzMqWgbtIRkrwkG8O1p1AEStdscHLCG0tKO0n-dlysDnly3XkMOzPcA-WTtMPboCDox-uVyb6k8Qdd4tf_D3VnG3lO-v6-DBZLWv_efTteHJB_Z0uLmpCEpmOifkbQw8rcDxg");'
              ></div>
            </div>
          </div>
          <div class="flex items-center justify-center p-4">
            <a href="#" class="flex size-10 items-center justify-center">
              <div class="text-white" data-icon="CaretLeft" data-size="18px" data-weight="regular">
                <svg xmlns="http://www.w3.org/2000/svg" width="18px" height="18px" fill="currentColor" viewBox="0 0 256 256">
                  <path d="M165.66,202.34a8,8,0,0,1-11.32,11.32l-80-80a8,8,0,0,1,0-11.32l80-80a8,8,0,0,1,11.32,11.32L91.31,128Z"></path>
                </svg>
              </div>
            </a>
            <a class="text-sm font-bold leading-normal tracking-[0.015em] flex size-10 items-center justify-center text-white rounded-full bg-[#29382f]" href="#">1</a>
            <a class="text-sm font-normal leading-normal flex size-10 items-center justify-center text-white rounded-full" href="#">2</a>
            <a class="text-sm font-normal leading-normal flex size-10 items-center justify-center text-white rounded-full" href="#">3</a>
            <a class="text-sm font-normal leading-normal flex size-10 items-center justify-center text-white rounded-full" href="#">4</a>
            <a class="text-sm font-normal leading-normal flex size-10 items-center justify-center text-white rounded-full" href="#">5</a>
            <a href="#" class="flex size-10 items-center justify-center">
              <div class="text-white" data-icon="CaretRight" data-size="18px" data-weight="regular">
                <svg xmlns="http://www.w3.org/2000/svg" width="18px" height="18px" fill="currentColor" viewBox="0 0 256 256">
                  <path d="M181.66,133.66l-80,80a8,8,0,0,1-11.32-11.32L164.69,128,90.34,53.66a8,8,0,0,1,11.32-11.32l80,80A8,8,0,0,1,181.66,133.66Z"></path>
                </svg>
              </div>
            </a>
          </div>
        </div>
      </div>
    </div>
</template>