<template>
  <div id="app">
    <div id="__next">
      <div class="overflow-hidden w-full h-full relative">
        <div class="flex h-full flex-1 flex-col md:pl-[260px]">
          <div
            class="sticky top-0 z-10 flex items-center border-b border-white/20 bg-gray-800 pl-1 pt-1 text-gray-200 sm:pl-3 md:hidden"
          >
            <div>
              <button
                @click="showSlideMethod"
                type="button"
                class="-ml-0.5 -mt-0.5 inline-flex h-10 w-10 items-center justify-center rounded-md hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white dark:hover:text-white"
              >
                <span class="sr-only">Open sidebar</span>
                <svg
                  stroke="currentColor"
                  fill="none"
                  stroke-width="1.5"
                  viewBox="0 0 24 24"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  class="h-6 w-6"
                  height="1em"
                  width="1em"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <line x1="3" y1="12" x2="21" y2="12"></line>
                  <line x1="3" y1="6" x2="21" y2="6"></line>
                  <line x1="3" y1="18" x2="21" y2="18"></line>
                </svg>
              </button>
            </div>
            <h1 class="flex-1 text-center text-base font-normal">
              {{ chatTitle }}
            </h1>
            <button @click.stop="newChat" type="button" class="px-3">
              <svg
                stroke="currentColor"
                fill="none"
                stroke-width="1.5"
                viewBox="0 0 24 24"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="h-6 w-6"
                height="1em"
                width="1em"
                xmlns="http://www.w3.org/2000/svg"
              >
                <line x1="12" y1="5" x2="12" y2="19"></line>
                <line x1="5" y1="12" x2="19" y2="12"></line>
              </svg>
            </button>
          </div>

          <main
            class="relative h-full w-full transition-width flex flex-col overflow-hidden items-stretch flex-1"
          >
            <div class="flex-1 overflow-hidden">
              <div
                class="react-scroll-to-bottom--css-ncqif-79elbk h-full dark:bg-gray-800"
              >
                <div
                  ref="chatContainer"
                  class="react-scroll-to-bottom--css-krija-1n7m0yu"
                >
                  <div
                    class="flex flex-col items-center text-sm dark:bg-gray-800"
                  >
                    <template v-for="(conv, idx) in conversation">
                      <div
                        v-if="conv.speaker == 'human'"
                        class="w-full border-b border-black/10 dark:border-gray-900/50 text-gray-800 dark:text-gray-100 group dark:bg-gray-800"
                      >
                        <div
                          class="text-base gap-4 md:gap-6 m-auto md:max-w-2xl lg:max-w-2xl xl:max-w-3xl p-4 md:py-6 flex lg:px-0"
                        >
                          <div
                            class="w-[30px] flex flex-col relative items-end"
                          >
                            <div class="relative flex">
                              <span
                                style="
                                  box-sizing: border-box;
                                  display: inline-block;
                                  overflow: hidden;
                                  width: initial;
                                  height: initial;
                                  background: none;
                                  opacity: 1;
                                  border: 0px;
                                  margin: 0px;
                                  padding: 0px;
                                  position: relative;
                                  max-width: 100%;
                                "
                              >
                                <span
                                  style="
                                    box-sizing: border-box;
                                    display: block;
                                    width: initial;
                                    height: initial;
                                    background: none;
                                    opacity: 1;
                                    border: 0px;
                                    margin: 0px;
                                    padding: 0px;
                                    max-width: 100%;
                                  "
                                >
                                  <img
                                    aria-hidden="true"
                                    :src="require('./assets/imgs/user.png')"
                                    alt="huamn"
                                    style="
                                      display: block;
                                      max-width: 100%;
                                      width: initial;
                                      height: initial;
                                      background: none;
                                      opacity: 1;
                                      border: 0px;
                                      margin: 0px;
                                      padding: 0px;
                                    "
                                  />
                                </span>
                              </span>
                            </div>
                          </div>
                          <div
                            class="relative flex w-[calc(100%-50px)] flex-col gap-1 md:gap-3 lg:w-[calc(100%-115px)]"
                          >
                            <div class="flex flex-grow flex-col gap-3">
                              <div
                                class="min-h-[20px] flex flex-col items-start gap-4 whitespace-pre-wrap"
                              >
                                {{ conv.speech }}
                              </div>
                            </div>
                            <div
                              v-if="false"
                              class="text-gray-400 flex self-end lg:self-center justify-center mt-2 gap-3 md:gap-4 lg:gap-1 lg:absolute lg:top-0 lg:translate-x-full lg:right-0 lg:mt-0 lg:pl-2 visible"
                            >
                              <button
                                class="p-1 rounded-md hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-gray-200 disabled:dark:hover:text-gray-400 md:invisible md:group-hover:visible"
                              >
                                <svg
                                  stroke="currentColor"
                                  fill="none"
                                  stroke-width="2"
                                  viewBox="0 0 24 24"
                                  stroke-linecap="round"
                                  stroke-linejoin="round"
                                  class="h-4 w-4"
                                  height="1em"
                                  width="1em"
                                  xmlns="http://www.w3.org/2000/svg"
                                >
                                  <path
                                    d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"
                                  ></path>
                                  <path
                                    d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"
                                  ></path>
                                </svg>
                              </button>
                            </div>
                            <div class="flex justify-between"></div>
                          </div>
                        </div>
                      </div>

                      <div
                        v-if="conv.speaker == 'ai'"
                        class="w-full border-b border-black/10 dark:border-gray-900/50 text-gray-800 dark:text-gray-100 group bg-gray-50 dark:bg-[#444654]"
                      >
                        <div
                          class="text-base gap-4 md:gap-6 m-auto md:max-w-2xl lg:max-w-2xl xl:max-w-3xl p-4 md:py-6 flex lg:px-0"
                        >
                          <div
                            class="w-[30px] flex flex-col relative items-end"
                          >
                            <div
                              class="relative h-[30px] w-[30px] p-1 rounded-sm text-white flex items-center justify-center"
                              style="background-color: rgb(62, 110, 250)"
                            >
                              <svg id="a" data-name="frame" xmlns="http://www.w3.org/2000/svg" width="194.1" height="175.2" viewBox="0 0 194.1 175.2">
                                <ellipse cx="99" cy="107" rx="84.6" ry="57.7" style="fill: none; stroke: #ababab; stroke-miterlimit: 10; stroke-width: 21px;"/>
                                <path d="m174.9,65.7s-1.1,9.4-2.4,13.3-4.5,11.1-4.5,11.1c2.2,3.4,3.7,7.7,3.7,7.7,0,0,5.5-8,6.8-11.6s3-13.2,2.9-13.4c-1.7-2.6-6.5-7.1-6.5-7.1Z" style="fill: #3e6efa;"/>
                                <ellipse cx="87.7" cy="79.7" rx="84.6" ry="59.9" transform="translate(-30 65.7) rotate(-35.5)" style="fill: none; stroke: #fff; stroke-miterlimit: 10; stroke-width: 21px;"/>
                              </svg>
                            </div>

                            <div
                              v-if="conv.speeches.length > 1"
                              class="text-xs flex items-center justify-center gap-1 invisible absolute left-0 top-2 -ml-4 -translate-x-full group-hover:visible"
                            >
                              <button
                                @click.stop="last(conv)"
                                :disabled="!(conv.idx > 0)"
                                class="dark:text-white disabled:text-gray-300 dark:disabled:text-gray-400"
                              >
                                <svg
                                  stroke="currentColor"
                                  fill="none"
                                  stroke-width="1.5"
                                  viewBox="0 0 24 24"
                                  stroke-linecap="round"
                                  stroke-linejoin="round"
                                  class="h-3 w-3"
                                  height="1em"
                                  width="1em"
                                  xmlns="http://www.w3.org/2000/svg"
                                >
                                  <polyline points="15 18 9 12 15 6"></polyline>
                                </svg>
                              </button>
                              <span class="flex-grow flex-shrink-0"
                                >{{ conv.idx + 1 }} /
                                {{ conv.speeches.length }}</span
                              >
                              <button
                                @click.stop="next(conv)"
                                :disabled="
                                  !(conv.idx < conv.speeches.length - 1)
                                "
                                class="dark:text-white disabled:text-gray-300 dark:disabled:text-gray-400"
                              >
                                <svg
                                  stroke="currentColor"
                                  fill="none"
                                  stroke-width="1.5"
                                  viewBox="0 0 24 24"
                                  stroke-linecap="round"
                                  stroke-linejoin="round"
                                  class="h-3 w-3"
                                  height="1em"
                                  width="1em"
                                  xmlns="http://www.w3.org/2000/svg"
                                >
                                  <polyline points="9 18 15 12 9 6"></polyline>
                                </svg>
                              </button>
                            </div>
                          </div>
                          <div
                            class="relative flex w-[calc(100%-50px)] flex-col gap-1 md:gap-3 lg:w-[calc(100%-115px)]"
                          >
                            <div class="flex flex-grow flex-col gap-3">
                              <!--  whitespace-pre-wrap -->
                              <div
                                class="min-h-[20px] flex flex-col items-start gap-4"
                              >
                                <div
                                  v-html="
                                    mdToHtml(conv.speeches[conv.idx], conv)
                                  "
                                  :class="{ 'result-streaming': conv.loading }"
                                  class="markdown prose-r w-full break-words dark:prose-invert light"
                                ></div>
                              </div>
                            </div>
                            <div class="flex justify-between">
                              <div
                                class="text-gray-400 flex self-end lg:self-center justify-center mt-2 gap-3 md:gap-4 lg:gap-1 lg:absolute lg:top-0 lg:translate-x-full lg:right-0 lg:mt-0 lg:pl-2 visible"
                              >
                              <button
                                  @click.stop="copy(idx, conv, -1)"
                                  class="p-1 rounded-md hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-gray-200 disabled:dark:hover:text-gray-400"
                                >
                                <svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>
                                </button>

                                <button
                                  @click.stop="suitable(idx, conv, 1)"
                                  v-if="
                                    conv.suitable[conv.idx] == 0 ||
                                    conv.suitable[conv.idx] == 1
                                  "
                                  :class="{
                                    suitable_selected:
                                      conv.suitable[conv.idx] == 1,
                                  }"
                                  class="p-1 rounded-md hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-gray-200 disabled:dark:hover:text-gray-400"
                                >
                                  <svg
                                    stroke="currentColor"
                                    fill="none"
                                    stroke-width="2"
                                    viewBox="0 0 24 24"
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    class="h-4 w-4"
                                    height="1em"
                                    width="1em"
                                    xmlns="http://www.w3.org/2000/svg"
                                  >
                                    <path
                                      d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"
                                    ></path>
                                  </svg>
                                </button>
                                <button
                                  @click.stop="suitable(idx, conv, -1)"
                                  v-if="
                                    conv.suitable[conv.idx] == 0 ||
                                    conv.suitable[conv.idx] == -1
                                  "
                                  :class="{
                                    suitable_selected:
                                      conv.suitable[conv.idx] == -1,
                                  }"
                                  class="p-1 rounded-md hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-gray-200 disabled:dark:hover:text-gray-400"
                                >
                                  <svg
                                    stroke="currentColor"
                                    fill="none"
                                    stroke-width="2"
                                    viewBox="0 0 24 24"
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    class="h-4 w-4"
                                    height="1em"
                                    width="1em"
                                    xmlns="http://www.w3.org/2000/svg"
                                  >
                                    <path
                                      d="M10 15v4a3 3 0 0 0 3 3l4-9V2H5.72a2 2 0 0 0-2 1.7l-1.38 9a2 2 0 0 0 2 2.3zm7-13h2.67A2.31 2.31 0 0 1 22 4v7a2.31 2.31 0 0 1-2.33 2H17"
                                    ></path>
                                  </svg>
                                </button>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </template>

                    <div
                      v-if="conversation.length == 0"
                      class="text-gray-800 w-full md:max-w-2xl lg:max-w-3xl md:h-full md:flex md:flex-col px-6 dark:text-gray-100"
                    >
                      <h1
                        class="text-4xl text-center mt-6 sm:mt-[20vh] ml-auto mr-auto mb-10 sm:mb-16 flex gap-2 items-center justify-center main-title"
                      >
                        ChatGLM
                        <span class="rounded-md bg-yellow-200 px-1.5 py-0.5 text-xs font-medium text-gray-800">v2</span>
                        <!-- <span class="rounded-md bg-yellow-200 px-1.5 py-0.5 text-xs font-medium uppercase text-gray-800">Engineering</span> -->
                      </h1>
                      <div class="md:flex items-start text-center gap-3.5">
                        <div
                          class="flex flex-col mb-8 md:mb-auto gap-3.5 flex-1"
                        >
                          <h2
                            class="flex gap-3 items-center m-auto text-lg font-normal md:flex-col md:gap-2"
                          >
                            <svg
                              stroke="currentColor"
                              fill="none"
                              stroke-width="1.5"
                              viewBox="0 0 24 24"
                              stroke-linecap="round"
                              stroke-linejoin="round"
                              class="h-6 w-6"
                              height="1em"
                              width="1em"
                              xmlns="http://www.w3.org/2000/svg"
                            >
                              <circle cx="12" cy="12" r="5"></circle>
                              <line x1="12" y1="1" x2="12" y2="3"></line>
                              <line x1="12" y1="21" x2="12" y2="23"></line>
                              <line
                                x1="4.22"
                                y1="4.22"
                                x2="5.64"
                                y2="5.64"
                              ></line>
                              <line
                                x1="18.36"
                                y1="18.36"
                                x2="19.78"
                                y2="19.78"
                              ></line>
                              <line x1="1" y1="12" x2="3" y2="12"></line>
                              <line x1="21" y1="12" x2="23" y2="12"></line>
                              <line
                                x1="4.22"
                                y1="19.78"
                                x2="5.64"
                                y2="18.36"
                              ></line>
                              <line
                                x1="18.36"
                                y1="5.64"
                                x2="19.78"
                                y2="4.22"
                              ></line>
                            </svg>
                            示例
                          </h2>
                          <ul
                            class="flex flex-col gap-3.5 w-full sm:max-w-md m-auto"
                          >
                            <button
                              @click="inputChat('GPT4是什么？')"
                              class="w-full bg-gray-50 dark:bg-white/5 p-3 rounded-md hover:bg-gray-200 dark:hover:bg-gray-900"
                            >
                              "GPT4是什么？" →
                            </button>
                            <button
                              @click="
                                inputChat(
                                  '请画一张小鸟飞翔的图片'
                                )
                              "
                              class="w-full bg-gray-50 dark:bg-white/5 p-3 rounded-md hover:bg-gray-200 dark:hover:bg-gray-900"
                            >
                              "请画一张小鸟飞翔的图片" →
                            </button>
                            <button
                              @click="
                                inputChat(
                                  '明天上海天气如何？'
                                )
                              "
                              class="w-full bg-gray-50 dark:bg-white/5 p-3 rounded-md hover:bg-gray-200 dark:hover:bg-gray-900"
                            >
                              "明天上海天气如何？" →
                            </button>
                            <button
                            @click="
                              inputChat(
                                '今天是农历几月几号？'
                              )
                            "
                            class="w-full bg-gray-50 dark:bg-white/5 p-3 rounded-md hover:bg-gray-200 dark:hover:bg-gray-900"
                          >
                            "今天是农历几月几号？" →
                          </button>
                          </ul>
                        </div>
                        <div
                          class="flex flex-col mb-8 md:mb-auto gap-3.5 flex-1"
                        >
                          <h2
                            class="flex gap-3 items-center m-auto text-lg font-normal md:flex-col md:gap-2"
                          >
                            <svg
                              xmlns="http://www.w3.org/2000/svg"
                              fill="none"
                              viewBox="0 0 24 24"
                              stroke-width="1.5"
                              stroke="currentColor"
                              aria-hidden="true"
                              class="h-6 w-6"
                            >
                              <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z"
                              ></path>
                            </svg>
                            能力
                          </h2>
                          <ul
                            class="flex flex-col gap-3.5 w-full sm:max-w-md m-auto"
                          >
                            <li
                              class="w-full bg-gray-50 dark:bg-white/5 p-3 rounded-md"
                            >
                              可以记住用户之前输入的内容，即支持上下文对话
                            </li>
                            <li
                              class="w-full bg-gray-50 dark:bg-white/5 p-3 rounded-md"
                            >
                              可以通过用户的需求生成图片
                            </li>
                            <li
                              class="w-full bg-gray-50 dark:bg-white/5 p-3 rounded-md"
                            >
                              可以通过网络搜索信息
                            </li>
                          </ul>
                        </div>
                        <div
                          class="flex flex-col mb-8 md:mb-auto gap-3.5 flex-1"
                        >
                          <h2
                            class="flex gap-3 items-center m-auto text-lg font-normal md:flex-col md:gap-2"
                          >
                            <svg
                              stroke="currentColor"
                              fill="none"
                              stroke-width="1.5"
                              viewBox="0 0 24 24"
                              stroke-linecap="round"
                              stroke-linejoin="round"
                              class="h-6 w-6"
                              height="1em"
                              width="1em"
                              xmlns="http://www.w3.org/2000/svg"
                            >
                              <path
                                d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"
                              ></path>
                              <line x1="12" y1="9" x2="12" y2="13"></line>
                              <line x1="12" y1="17" x2="12.01" y2="17"></line>
                            </svg>
                            限制
                          </h2>
                          <ul
                            class="flex flex-col gap-3.5 w-full sm:max-w-md m-auto"
                          >
                            <li
                              class="w-full bg-gray-50 dark:bg-white/5 p-3 rounded-md"
                            >
                              有时会生成错误的答案
                            </li>
                            <li
                              class="w-full bg-gray-50 dark:bg-white/5 p-3 rounded-md"
                            >
                              可能会触发自己不想要的功能，例如生成图片或网络搜索
                            </li>

                            <li
                              class="w-full bg-gray-50 dark:bg-white/5 p-3 rounded-md"
                            >
                              用户输入的指令有时可能无法记住或再次使用
                            </li>
                          </ul>
                        </div>
                      </div>
                    </div>

                    <div class="w-full h-32 md:h-48 flex-shrink-0"></div>
                  </div>

                  <transition name="el-fade-in-linear">
                    <button
                      v-show="isShowGoBottom"
                      @click="handleScrollBottom"
                      class="cursor-pointer absolute right-6 bottom-[124px] md:bottom-[120px] z-10 rounded-full border border-gray-200 bg-gray-50 text-gray-600 dark:border-white/10 dark:bg-white/10 dark:text-gray-200"
                    >
                      <svg
                        stroke="currentColor"
                        fill="none"
                        stroke-width="2"
                        viewBox="0 0 24 24"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        class="h-4 w-4 m-1"
                        height="1em"
                        width="1em"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <line x1="12" y1="5" x2="12" y2="19"></line>
                        <polyline points="19 12 12 19 5 12"></polyline>
                      </svg>
                    </button>
                  </transition>
                </div>
              </div>
            </div>

            <div
              class="absolute bottom-0 left-0 w-full border-t md:border-t-0 dark:border-white/20 md:border-transparent md:dark:border-transparent md:bg-vert-light-gradient bg-white dark:bg-gray-800 md:!bg-transparent dark:md:bg-vert-dark-gradient"
            >
              <form
                class="stretch mx-2 flex flex-row gap-3 pt-2 last:mb-2 md:last:mb-6 lg:mx-auto lg:max-w-3xl lg:pt-6"
              >
                <div class="relative flex h-full flex-1 md:flex-col">
                  <div
                    class="flex ml-1 md:w-full md:m-auto md:mb-2 gap-0 md:gap-2 justify-center"
                  >
                    <button
                      v-if="!convLoading && conversation.length > 0"
                      @click.stop.prevent="chatRepeat"
                      id="chatRepeat"
                      class="btn flex justify-center gap-2 btn-neutral border-0 md:border"
                    >
                      <svg
                        stroke="currentColor"
                        fill="none"
                        stroke-width="1.5"
                        viewBox="0 0 24 24"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        class="h-3 w-3"
                        height="1em"
                        width="1em"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <polyline points="1 4 1 10 7 10"></polyline>
                        <polyline points="23 20 23 14 17 14"></polyline>
                        <path
                          d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 0 1 3.51 15"
                        ></path>
                      </svg>
                      <p class="none">重新生成对话</p>
                    </button>

                    <button
                      v-if="convLoading"
                      @click.stop.prevent="stopChat"
                      id="stopChat"
                      class="btn relative btn-neutral border-0 md:border"
                    >
                      <div
                        class="flex w-full items-center justify-center gap-2"
                      >
                        <svg
                          stroke="currentColor"
                          fill="none"
                          stroke-width="1.5"
                          viewBox="0 0 24 24"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          class="h-3 w-3"
                          height="1em"
                          width="1em"
                          xmlns="http://www.w3.org/2000/svg"
                        >
                          <rect
                            x="3"
                            y="3"
                            width="18"
                            height="18"
                            rx="2"
                            ry="2"
                          ></rect></svg
                        >停止生成对话
                      </div>
                    </button>
                  </div>
                  <div
                    class="flex flex-col w-full py-[10px] flex-grow md:py-4 md:pl-4 relative border border-black/10 bg-white dark:border-gray-900/50 dark:text-white dark:bg-gray-700 rounded-xl shadow-xs dark:shadow-xs"
                    style="border-radius: 15px;
                    box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.05);"
                    >
                    <textarea
                      v-model="chatMsg"
                      ref="inputChat"
                      @keydown="judgeInput"
                      tabindex="0"
                      data-id="root"
                      style="max-height: 200px;
                        height: 24px;
                        overflow-y: hidden;"
                      rows="1"
                      placeholder="发送信息..."
                      class="m-0 w-full resize-none border-0 bg-transparent p-0 pl-2 pr-7 focus:ring-0 focus-visible:ring-0 dark:bg-transparent md:pl-0"
                    ></textarea>
                    <button
                      @click.stop.prevent="send"
                      :disabled="convLoading"
                      style="margin-right: 10px;"
                      class="absolute p-1 rounded-md bottom-[10px] md:bottom-3 md:p-2 md:right-3 dark:hover:bg-gray-900 dark:disabled:hover:bg-transparent right-1 disabled:text-gray-400 enabled:bg-brand-purple text-white transition-colors disabled:opacity-40"
                    >
                      <div
                        v-if="convLoading"
                        class="text-2xl"
                        style="line-height: 1.3rem"
                      >
                        <span class="load_dot1">·</span
                        ><span class="load_dot2">·</span
                        ><span class="load_dot3">·</span>
                      </div>
                      <svg
                        v-else
                        stroke="currentColor"
                        fill="none"
                        stroke-width="2"
                        viewBox="0 0 24 24"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        class="h-4 w-4 mr-1"
                        height="1em"
                        width="1em"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <line x1="22" y1="2" x2="11" y2="13"></line>
                        <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                      </svg>
                    </button>
                  </div>
                </div>
              </form>
              <div
                class="px-3 pt-2 pb-3 text-center text-xs text-black/50 dark:text-white/50 md:px-4 md:pt-3 md:pb-6"
              >
                本项目使用
                <a
                  href="https://github.com/THUDM/ChatGLM-6B"
                  target="_blank"
                  rel="noreferrer"
                  class="underline"
                  >ChatGLM-6B</a
                >，
                <a
                  href="https://github.com/THUDM/ChatGLM2-6B"
                  target="_blank"
                  rel="noreferrer"
                  class="underline"
                  >ChatGLM2-6B</a
                >，
                <a
                  href="https://gitee.com/MIEAPP/chatai-vue"
                  target="_blank"
                  rel="noreferrer"
                  class="underline"
                  >chatai-vue</a
                >，
                <a
                  href="https://github.com/LemonQu-GIT/ChatGLM-6B-Engineering"
                  target="_blank"
                  rel="noreferrer"
                  class="underline"
                  >ChatGLM-6B-Engineering</a
                >
              </div>
            </div>
          </main>
        </div>

        <div
          class="dark hidden bg-gray-900 md:fixed md:inset-y-0 md:flex md:w-[260px] md:flex-col"
        >
          <div class="flex h-full min-h-0 flex-col">
            <div
              ref="menu"
              class="scrollbar-trigger flex h-full w-full flex-1 items-start border-white/20"
            >
              <nav
                ref="navEle"
                class="flex h-full flex-1 flex-col space-y-1 p-2"
              >
                <a
                  @click.stop="newChat"
                  class="flex py-3 px-3 items-center gap-3 rounded-md hover:bg-gray-500/10 transition-colors duration-200 text-white cursor-pointer text-sm mb-2 flex-shrink-0 border border-white/20"
                >
                  <svg
                    stroke="currentColor"
                    fill="none"
                    stroke-width="2"
                    viewBox="0 0 24 24"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    class="h-4 w-4"
                    height="1em"
                    width="1em"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <line x1="12" y1="5" x2="12" y2="19"></line>
                    <line x1="5" y1="12" x2="19" y2="12"></line>
                  </svg>
                  创建新对话
                </a>
                
                <div
                  class="flex-col flex-1 overflow-y-auto border-b border-white/20"
                  style="padding-bottom: 5px"
                >
                  <div class="flex flex-col gap-2 text-gray-100 text-sm">
                    <template v-for="(conversation, cidx) in conversations">
                      <div
                        v-if="conversation.editable"
                        class="m-focus flex py-3 px-3 items-center gap-3 relative rounded-md cursor-pointer hover:pr-14 break-all pr-14 bg-gray-800 hover:bg-gray-800"
                      >
                        <svg
                          stroke="currentColor"
                          fill="none"
                          stroke-width="2"
                          viewBox="0 0 24 24"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          class="h-4 w-4 flex-shrink-0"
                          height="1em"
                          width="1em"
                          xmlns="http://www.w3.org/2000/svg"
                        >
                          <path
                            d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"
                          ></path>
                        </svg>
                        <input
                          id="titleInput"
                          v-model="convTitletmp"
                          @blur="titleInputBlur(cidx, conversation)"
                          type="text"
                          class="text-sm border-none bg-transparent p-0 m-0 w-full mr-0"
                          autofocus="true"
                        />
                        <div
                          class="absolute flex right-1 z-10 text-gray-300 visible"
                        >
                          <button
                            @click="changeConvTitle(cidx, conversation)"
                            class="p-1 hover:text-white"
                          >
                            <svg
                              stroke="currentColor"
                              fill="none"
                              stroke-width="2"
                              viewBox="0 0 24 24"
                              stroke-linecap="round"
                              stroke-linejoin="round"
                              class="h-4 w-4"
                              height="1em"
                              width="1em"
                              xmlns="http://www.w3.org/2000/svg"
                            >
                              <polyline points="20 6 9 17 4 12"></polyline>
                            </svg>
                          </button>
                          <button
                            @click="cancelChangeConvTitle(cidx, conversation)"
                            class="p-1 hover:text-white"
                          >
                            <svg
                              stroke="currentColor"
                              fill="none"
                              stroke-width="2"
                              viewBox="0 0 24 24"
                              stroke-linecap="round"
                              stroke-linejoin="round"
                              class="h-4 w-4"
                              height="1em"
                              width="1em"
                              xmlns="http://www.w3.org/2000/svg"
                            >
                              <line x1="18" y1="6" x2="6" y2="18"></line>
                              <line x1="6" y1="6" x2="18" y2="18"></line>
                            </svg>
                          </button>
                        </div>
                      </div>

                      <a
                        v-else-if="conversation.delete"
                        @blur="cancelDelConv(cidx, conversation)"
                        class="m-focus flex py-3 px-3 items-center gap-3 relative rounded-md cursor-pointer break-all pr-14 bg-gray-800 hover:bg-gray-800 group"
                      >
                        <svg
                          stroke="currentColor"
                          fill="none"
                          stroke-width="2"
                          viewBox="0 0 24 24"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          class="h-4 w-4"
                          height="1em"
                          width="1em"
                          xmlns="http://www.w3.org/2000/svg"
                        >
                          <polyline points="3 6 5 6 21 6"></polyline>
                          <path
                            d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"
                          ></path>
                          <line x1="10" y1="11" x2="10" y2="17"></line>
                          <line x1="14" y1="11" x2="14" y2="17"></line>
                        </svg>
                        <div
                          class="flex-1 text-ellipsis max-h-5 overflow-hidden break-all relative"
                        >
                          删除 "{{ conversation.title }}"?
                          <div
                            class="absolute inset-y-0 right-0 w-8 z-10 bg-gradient-to-l from-gray-800"
                          ></div>
                        </div>
                        <div
                          class="absolute flex right-1 z-10 text-gray-300 visible"
                        >
                          <button
                            @click="delConv(cidx)"
                            class="p-1 hover:text-white"
                          >
                            <svg
                              stroke="currentColor"
                              fill="none"
                              stroke-width="2"
                              viewBox="0 0 24 24"
                              stroke-linecap="round"
                              stroke-linejoin="round"
                              class="h-4 w-4"
                              height="1em"
                              width="1em"
                              xmlns="http://www.w3.org/2000/svg"
                            >
                              <polyline points="20 6 9 17 4 12"></polyline>
                            </svg>
                          </button>
                          <button
                            @click="cancelDelConv(cidx, conversation)"
                            class="p-1 hover:text-white"
                          >
                            <svg
                              stroke="currentColor"
                              fill="none"
                              stroke-width="2"
                              viewBox="0 0 24 24"
                              stroke-linecap="round"
                              stroke-linejoin="round"
                              class="h-4 w-4"
                              height="1em"
                              width="1em"
                              xmlns="http://www.w3.org/2000/svg"
                            >
                              <line x1="18" y1="6" x2="6" y2="18"></line>
                              <line x1="6" y1="6" x2="18" y2="18"></line>
                            </svg>
                          </button>
                        </div>
                      </a>

                      <a
                        v-else
                        @click.stop.prevent="
                          selectConversation(conversation, true)
                        "
                        :class="{
                          'bg-gray-800 hover:bg-gray-800 pr-14':
                            conversation.selected,
                          'hover:bg-[#2A2B32] hover:pr-4':
                            !conversation.selected,
                        }"
                        class="flex py-3 px-3 items-center gap-3 relative rounded-md cursor-pointer break-all group"
                      >
                        <svg
                          stroke="currentColor"
                          fill="none"
                          stroke-width="2"
                          viewBox="0 0 24 24"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          class="h-4 w-4"
                          height="1em"
                          width="1em"
                          xmlns="http://www.w3.org/2000/svg"
                        >
                          <path
                            d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"
                          ></path>
                        </svg>
                        <div
                          class="flex-1 text-ellipsis max-h-5 overflow-hidden break-all relative"
                        >
                          {{ conversation.title }}
                          <div
                            :class="{
                              'from-gray-800': conversation.selected,
                              'from-gray-900 group-hover:from-[#2A2B32]':
                                !conversation.selected,
                            }"
                            class="absolute inset-y-0 right-0 w-8 z-10 bg-gradient-to-l"
                          ></div>
                        </div>
                        <div
                          v-show="conversation.selected"
                          class="absolute flex right-1 z-10 text-gray-300 visible"
                        >
                          <button
                            @click="editTitle(cidx, conversation)"
                            class="p-1 hover:text-white"
                          >
                            <svg
                              stroke="currentColor"
                              fill="none"
                              stroke-width="2"
                              viewBox="0 0 24 24"
                              stroke-linecap="round"
                              stroke-linejoin="round"
                              class="h-4 w-4"
                              height="1em"
                              width="1em"
                              xmlns="http://www.w3.org/2000/svg"
                            >
                              <path d="M12 20h9"></path>
                              <path
                                d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"
                              ></path>
                            </svg>
                          </button>
                          <button
                            @click="conversation.delete = true"
                            class="p-1 hover:text-white"
                          >
                            <svg
                              stroke="currentColor"
                              fill="none"
                              stroke-width="2"
                              viewBox="0 0 24 24"
                              stroke-linecap="round"
                              stroke-linejoin="round"
                              class="h-4 w-4"
                              height="1em"
                              width="1em"
                              xmlns="http://www.w3.org/2000/svg"
                            >
                              <polyline points="3 6 5 6 21 6"></polyline>
                              <path
                                d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"
                              ></path>
                              <line x1="10" y1="11" x2="10" y2="17"></line>
                              <line x1="14" y1="11" x2="14" y2="17"></line>
                            </svg>
                          </button>
                        </div>
                      </a>
                    </template>
                  </div>
                </div>

                <a
                  v-if="conversations.length > 0"
                  @click.stop.prevent="clearConversations"
                  class="flex py-3 px-3 items-center gap-3 rounded-md hover:bg-gray-500/10 transition-colors duration-200 text-white cursor-pointer text-sm"
                >
                  <svg
                    stroke="currentColor"
                    fill="none"
                    stroke-width="2"
                    viewBox="0 0 24 24"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    class="h-4 w-4"
                    height="1em"
                    width="1em"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <polyline points="3 6 5 6 21 6"></polyline>
                    <path
                      d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"
                    ></path>
                    <line x1="10" y1="11" x2="10" y2="17"></line>
                    <line x1="14" y1="11" x2="14" y2="17"></line>
                  </svg>
                  删除所有对话
                </a>
                <a
                  v-if="theme == 'light'"
                  @click="changeTheme('dark')"
                  class="flex py-3 px-3 items-center gap-3 rounded-md hover:bg-gray-500/10 transition-colors duration-200 text-white cursor-pointer text-sm"
                >
                  <svg
                    stroke="currentColor"
                    fill="none"
                    stroke-width="2"
                    viewBox="0 0 24 24"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    class="h-4 w-4"
                    height="1em"
                    width="1em"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"
                    ></path>
                  </svg>
                  深色模式
                </a>

                <a
                  v-if="theme == 'dark'"
                  @click="changeTheme('light')"
                  class="flex py-3 px-3 items-center gap-3 rounded-md hover:bg-gray-500/10 transition-colors duration-200 text-white cursor-pointer text-sm"
                >
                  <svg
                    stroke="currentColor"
                    fill="none"
                    stroke-width="2"
                    viewBox="0 0 24 24"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    class="h-4 w-4"
                    height="1em"
                    width="1em"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <circle cx="12" cy="12" r="5"></circle>
                    <line x1="12" y1="1" x2="12" y2="3"></line>
                    <line x1="12" y1="21" x2="12" y2="23"></line>
                    <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
                    <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
                    <line x1="1" y1="12" x2="3" y2="12"></line>
                    <line x1="21" y1="12" x2="23" y2="12"></line>
                    <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
                    <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
                  </svg>
                  浅色模式</a
                >

                <a
                  href="https://github.com/THUDM/ChatGLM2-6B"
                  target="_blank"
                  class="flex py-3 px-3 items-center gap-3 rounded-md hover:bg-gray-500/10 transition-colors duration-200 text-white cursor-pointer text-sm"
                >
                  <svg
                    stroke="currentColor"
                    fill="none"
                    stroke-width="2"
                    viewBox="0 0 24 24"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    class="h-4 w-4"
                    height="1em"
                    width="1em"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <title>GitHub</title>
                    <path
                      d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"
                    />
                  </svg>

                  ChatGLM2-6B 源码</a
                >
                <a
                  href="https://github.com/LemonQu-GIT/ChatGLM-6B-Engineering"
                  target="_blank"
                  class="flex py-3 px-3 items-center gap-3 rounded-md hover:bg-gray-500/10 transition-colors duration-200 text-white cursor-pointer text-sm"
                >
                  <svg
                    stroke="currentColor"
                    fill="none"
                    stroke-width="2"
                    viewBox="0 0 24 24"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    class="h-4 w-4"
                    height="1em"
                    width="1em"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"
                    ></path>
                    <polyline points="15 3 21 3 21 9"></polyline>
                    <line x1="10" y1="14" x2="21" y2="3"></line>
                  </svg>
                  关于此项目</a
                >
                <a
                  @click.stop.prevent="moreBarShow"
                  class="flex py-3 px-3 items-center gap-3 rounded-md hover:bg-gray-500/10 transition-colors duration-200 text-white cursor-pointer text-sm"
                >
                <svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="9" y1="3" x2="9" y2="21"></line></svg>
              
              <div class="grow overflow-hidden text-ellipsis whitespace-nowrap text-left text-white">更多</div>
              <svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4 flex-shrink-0 text-gray-500" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="1"></circle><circle cx="19" cy="12" r="1"></circle><circle cx="5" cy="12" r="1"></circle></svg>
                </a>
                
              </nav>
            </div>
          </div>
        </div>
      </div>
      <div class="absolute top-0 left-0 right-0 z-[2]"></div>
    </div>

    <div v-show="showSlide" class="semi-portal" style="z-index: 1000">
      <div class="">
        <div class="semi-modal-mask"></div>
        <div role="none" class="semi-modal-wrap">
          <div
            class="semi-modal semi-modal-small"
            id="dialog-3"
            style="width: 0px"
          >
            <div
              role="dialog"
              aria-modal="true"
              aria-labelledby="semi-modal-title"
              aria-describedby="semi-modal-body"
              class="semi-modal-content"
            >
              <div class="semi-modal-body-wrapper">
                <div class="semi-modal-body" x-semi-prop="children">
                  <div class="fixed inset-0 z-40 flex">
                    <div
                      class="relative flex w-full max-w-xs flex-1 flex-col bg-gray-900 translate-x-0"
                      id="headlessui-dialog-panel-:r1:"
                      data-headlessui-state="open"
                    >
                      <div
                        class="absolute top-0 right-0 -mr-12 pt-2 opacity-100"
                      >
                        <button
                          @click="closeShowSlide"
                          type="button"
                          class="ml-1 flex h-10 w-10 items-center justify-center focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
                        >
                          <span class="sr-only">Close sidebar</span>
                          <svg
                            stroke="currentColor"
                            fill="none"
                            stroke-width="1.5"
                            viewBox="0 0 24 24"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            class="h-6 w-6 text-white"
                            height="1em"
                            width="1em"
                            xmlns="http://www.w3.org/2000/svg"
                          >
                            <line x1="18" y1="6" x2="6" y2="18"></line>
                            <line x1="6" y1="6" x2="18" y2="18"></line>
                          </svg>
                        </button>
                      </div>
                      <div
                        ref="slideNavContainer"
                        style="width: 320px"
                        class="flex h-full flex-1 items-start border-white/20"
                      ></div>
                    </div>
                    <div
                      @click="closeShowSlide"
                      style="width: calc(100% - 320px)"
                      class="flex-shrink-0"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    

    <div portal-container="">
      <span
        class="pointer-events-none fixed inset-0 z-[60] mx-auto my-2 flex max-w-[560px] flex-col items-stretch justify-start md:pb-5"
      >
      </span>
    </div>

    <!-- 弹窗 -->
    <div id="headlessui-portal-root" v-if="popupShow">
      <div data-headlessui-portal="">
        <button
          type="button"
          aria-hidden="true"
          style="
            position: fixed;
            top: 1px;
            left: 1px;
            width: 1px;
            height: 0px;
            padding: 0px;
            margin: -1px;
            overflow: hidden;
            clip: rect(0px, 0px, 0px, 0px);
            white-space: nowrap;
            border-width: 0px;
          "
        ></button>
        <div>
          <div
            class="relative z-50"
            id="headlessui-dialog-:r3:"
            role="dialog"
            aria-modal="true"
            data-headlessui-state="open"
            aria-labelledby="headlessui-dialog-title-:r5:"
          >
            <div
              class="fixed inset-0 bg-gray-500/90 transition-opacity dark:bg-gray-800/90"
            ></div>
            <div class="fixed inset-0 z-50 overflow-y-auto">
              <div
                class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0"
              >
                <div
                  v-if="popupShow"
                  class="relative transform overflow-hidden rounded-lg bg-white px-4 pt-5 pb-4 text-left shadow-xl transition-all dark:bg-gray-900 sm:my-8 sm:w-full sm:p-6 sm:max-w-lg opacity-100 translate-y-0 sm:scale-100"
                  id="headlessui-dialog-panel-:r1:"
                  data-headlessui-state="open"
                >
                  <div class="flex items-center sm:flex">
                    <div class="mt-3 text-center sm:mt-0 sm:text-left"></div>
                  </div>
                  <div class="prose dark:prose-invert">
                    <div class="mb-5">
                      <h2 class="!mt-4 font-normal !mb-2"><b>ChatGLM2-6B</b></h2>
                    </div>
                    <div class="w-full h-[1px] bg-gray-300 opacity-20"></div>
                    <h4 class="mb-4">
                      本项目基于 ChatGLM2-6B，UI 前端来源于 <br />
                      • https://gitee.com/MIEAPP/chatai-vue <br />
                    </h4>
                    <div class="flex gap-4 flex-col text-sm">
                      <div
                        class="flex p-4 bg-gray-50 dark:bg-white/5 rounded-md items-center gap-4 min-h-[71px]"
                      >
                        <div class="w-10 text-2xl text-center">🌐</div>
                        <div class="flex-1 leading-5">
                          本项目类 OpenAI Plugin ，欢迎提出意见与更好的想法
                        </div>
                      </div>
                      <div
                        class="flex p-4 bg-gray-50 dark:bg-white/5 rounded-md items-center gap-4 min-h-[71px]"
                      >
                        <div class="w-10 text-2xl text-center">🖌️</div>
                        <div class="flex-1 leading-5">仅供测试，欢迎反馈 Issue</div>
                      </div>
                    </div>
                    <div class="flex gap-4 mt-6">
                      <button
                        @click="closePopup"
                        class="btn flex justify-center gap-2 btn-primary ml-auto"
                        style="background-color: rgb(62, 110, 250)"
                      >
                        确定
                      </button>
                    </div>
                  </div>
                  <div
                    class="mt-5 flex flex-col gap-3 sm:mt-4 sm:flex-row-reverse"
                  ></div>
                </div>

                <div
                  v-if="false"
                  class="relative transform overflow-hidden rounded-lg bg-white px-4 pt-5 pb-4 text-left shadow-xl transition-all dark:bg-gray-900 sm:my-8 sm:w-full sm:p-6 sm:max-w-lg"
                  id="headlessui-dialog-panel-:r4:"
                  data-headlessui-state="open"
                >
                  <div class="flex items-center sm:flex">
                    <div
                      class="mr-4 flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full sm:h-10 sm:w-10 bg-green-100"
                    >
                      <svg
                        stroke="currentColor"
                        fill="none"
                        stroke-width="1.5"
                        viewBox="0 0 24 24"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        class="h-6 w-6 text-green-700"
                        height="1em"
                        width="1em"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <path
                          d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"
                        ></path>
                      </svg>
                    </div>
                    <div class="mt-3 text-center sm:mt-0 sm:text-left">
                      <h3
                        class="text-lg font-medium leading-6 text-gray-900 dark:text-gray-200"
                        id="headlessui-dialog-title-:r5:"
                        data-headlessui-state="open"
                      >
                        Provide additional feedback
                      </h3>
                    </div>
                  </div>
                  <form>
                    <textarea
                      id="feedback-other"
                      placeholder="What would the ideal answer have been?"
                      rows="3"
                      class="mt-4 mb-1 w-full rounded-md dark:bg-gray-800 dark:focus:border-white dark:focus:ring-white"
                      tabindex="0"
                      style="height: 89.4815px; overflow-y: hidden"
                    ></textarea>
                  </form>
                  <div
                    class="mt-5 flex flex-col gap-3 sm:mt-4 sm:flex-row-reverse"
                  >
                    <button class="btn flex justify-center gap-2 btn-neutral">
                      Submit feedback
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <button
          type="button"
          aria-hidden="true"
          style="
            position: fixed;
            top: 1px;
            left: 1px;
            width: 1px;
            height: 0px;
            padding: 0px;
            margin: -1px;
            overflow: hidden;
            clip: rect(0px, 0px, 0px, 0px);
            white-space: nowrap;
            border-width: 0px;
          "
        ></button>
      </div>
    </div>

    <!-- Tool bar-->
    <div id="headlessui-portal-root" v-if="moreBar">
      <div data-headlessui-portal="">
        <button
          type="button"
          aria-hidden="true"
          style="
            position: fixed;
            top: 1px;
            left: 1px;
            width: 1px;
            height: 0px;
            padding: 0px;
            margin: -1px;
            overflow: hidden;
            clip: rect(0px, 0px, 0px, 0px);
            white-space: nowrap;
            border-width: 0px;
          "
        ></button>
        <div>
          <div
            class="relative z-50"
            id="headlessui-dialog-:r3:"
            role="dialog"
            aria-modal="true"
            data-headlessui-state="open"
            aria-labelledby="headlessui-dialog-title-:r5:"
          >
          
            <div
              class="fixed inset-0 bg-gray-500/90 transition-opacity dark:bg-gray-800/90"
            ></div>
            <div class="fixed inset-0 z-50 overflow-y-auto">
              <div
                class="grid h-full w-full justify-center"
              >
                <div
                  v-if="moreBar"
                  class="col-auto relative transform overflow-hidden rounded-lg bg-white px-4 pt-5 pb-4 shadow-xl transition-all dark:bg-gray-900 sm:my-8 w-full sm:p-6 opacity-100 translate-y-0 sm:scale-100"
                  id="headlessui-dialog-panel-:r1:"
                  style="width: 700px;
                    height: auto;
                    align-items: center;
                    margin: auto;"
                >
                  <div class="flex items-center sm:flex">
                    <div class="mt-3 text-center sm:mt-0 sm:text-left"></div>
                  </div>
                      <h3 class="mt-1 font-normal"
                      style="margin-bottom: 20px;"
                      ><b>
                        更多
                        <span class="rounded-md bg-yellow-200 px-1.5 py-0.5 text-xs font-medium uppercase text-gray-800" style="margin-left: 7px;">Engineering</span>
                        <button
                          @click="moreBarClose"
                          class="gap-2"
                          style="float: right;"
                        >
                        <svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="text-gray-900 dark:text-gray-200" height="20" width="20" xmlns="http://www.w3.org/2000/svg"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                        </button>
                      </b></h3>
                    <div class="flex gap-4 flex-col text-sm">
                      
                      <div class="flex flex-col gap-3 text-sm text-gray-600 dark:text-gray-300">
                        <div class="border-b pb-3 last-of-type:border-b-0 dark:border-gray-700">
                          <div class="flex items-center justify-between">
                            <div>启用网络搜索</div>
                            <button
                              type="button"
                                role="switch"
                                aria-checked="true"
                                class="swi-button"
                                :class="{'switch-on': enableWeb, 'switch-off': !enableWeb}"
                                @click="switchButton('web')"
                              >
                                <span class="switch-thumb"></span>
                            </button>
                          </div>
                          <div class="mt-2 text-xs text-gray-500 dark:text-gray-600">允许调用后端的爬虫以访问已配置的网站数据，访问网站时不会通过你的 Cookie 访问</div>
                        </div>
                      </div>

                      <div class="flex flex-col gap-3 text-sm text-gray-600 dark:text-gray-300">
                        <div class="border-b pb-3 last-of-type:border-b-0 dark:border-gray-700">
                          <div class="flex items-center justify-between">
                            <div>启用天气</div>
                            <button
                              type="button"
                                role="switch"
                                aria-checked="true"
                                class="swi-button"
                                :class="{'switch-on': enableWeather, 'switch-off': !enableWeather}"
                                @click="switchButton('weather')"
                              >
                                <span class="switch-thumb"></span>
                            </button>
                          </div>
                          <div class="mt-2 text-xs text-gray-500 dark:text-gray-600">允许访问 <a href="https://www.qweather.com/" target="_blank" class="underline" rel="noreferrer">天气 API</a> 以获取天气数据</div>
                        </div>
                      </div>

                      <div class="flex flex-col gap-3 text-sm text-gray-600 dark:text-gray-300">
                        <div class="border-b pb-3 last-of-type:border-b-0 dark:border-gray-700">
                          <div class="flex items-center justify-between">
                            <div>启用时间查询</div>
                            <button
                              type="button"
                                role="switch"
                                aria-checked="true"
                                class="swi-button"
                                :class="{'switch-on': enableDate, 'switch-off': !enableDate}"
                                @click="switchButton('date')"
                              >
                                <span class="switch-thumb"></span>
                            </button>
                          </div>
                          <div class="mt-2 text-xs text-gray-500 dark:text-gray-600">允许获取当前阴历、阳历日期及时间</div>
                        </div>
                      </div>

                      <div class="flex flex-col gap-3 text-sm text-gray-600 dark:text-gray-300">
                        <div class="border-b pb-3 last-of-type:border-b-0 dark:border-gray-700">
                          <div class="flex items-center justify-between">
                            <div>附加文件</div>
                            <button class="btn relative btn-neutral">
                              <label for="file_upload">
                                <div class="flex w-full gap-2 items-center justify-center">上传文件</div>
                              </label>
                              <input id="file_upload" type="file" style="display: none" @change="handleFileUpload" accept="image/png, image/jpeg, .xls, .xlsx, .doc, .docx, .pdf, .txt, .py, .c, .cpp, .java, .html, .js">
                            </button>
                          </div>
                        </div>
                      </div>
                      
                      <div class="flex flex-col gap-3 text-sm text-gray-600 dark:text-gray-300">
                        <div class="border-b pb-3 last-of-type:border-b-0 dark:border-gray-700">
                          <div class="flex items-center justify-between">
                            <div>启用 Markmap</div>
                            <button
                              type="button"
                                role="switch"
                                aria-checked="true"
                                class="swi-button"
                                :class="{'switch-on': enableMarkmap, 'switch-off': !enableMarkmap}"
                                @click="switchButton('markmap')"
                              >
                                <span class="switch-thumb"></span>
                            </button>
                          </div>
                          <div class="mt-2 text-xs text-gray-500 dark:text-gray-600">允许调用后端调用本地 <a href="https://markmap.js.org/" target="_blank" class="underline" rel="noreferrer">Markmap</a> 以生成思维导图</div>
                        </div>
                      </div>

                      <div class="flex flex-col gap-3 text-sm text-gray-600 dark:text-gray-300">
                        <div class="border-b pb-3 last-of-type:border-b-0 dark:border-gray-700">
                          <div class="flex items-center justify-between">
                            <div>启用 Stable Diffusion</div>
                            <button
                              type="button"
                                role="switch"
                                aria-checked="true"
                                class="swi-button"
                                :class="{'switch-on': enableStableDiffusion, 'switch-off': !enableStableDiffusion}"
                                @click="switchButton('sd')"
                              >
                                <span class="switch-thumb"></span>
                            </button>
                          </div>
                          <div class="mt-2 text-xs text-gray-500 dark:text-gray-600">允许调用后端调用本地 <a href="https://github.com/AUTOMATIC1111/stable-diffusion-webui/tree/35b1775b32a07f1b7c9dccad61f7aa77027a00fa" target="_blank" class="underline" rel="noreferrer">Stable Diffusion API</a> 以生成图片  </div>
                        </div>
                      </div>

                    </div>
                  <div
                    class="mt-5 flex flex-col gap-3 sm:mt-4 sm:flex-row-reverse"
                  ></div>
                </div>
                <div
                  v-if="false"
                  class="relative transform overflow-hidden rounded-lg bg-white px-4 pt-5 pb-4 text-left shadow-xl transition-all dark:bg-gray-900 sm:my-8 sm:w-full sm:p-6 sm:max-w-lg"
                  id="headlessui-dialog-panel-:r4:"
                  data-headlessui-state="open"
                >
                  <div class="flex items-center sm:flex">
                    <div
                      class="mr-4 flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full sm:h-10 sm:w-10 bg-green-100"
                    >
                      <svg
                        stroke="currentColor"
                        fill="none"
                        stroke-width="1.5"
                        viewBox="0 0 24 24"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        class="h-6 w-6 text-green-700"
                        height="1em"
                        width="1em"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <path
                          d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"
                        ></path>
                      </svg>
                    </div>
                    <div class="mt-3 text-center sm:mt-0 sm:text-left">
                      <h3
                        class="text-lg font-medium leading-6 text-gray-900 dark:text-gray-200"
                        id="headlessui-dialog-title-:r5:"
                        data-headlessui-state="open"
                      >
                        Provide additional feedback
                      </h3>
                    </div>
                  </div>
                  <form>
                    <textarea
                      id="feedback-other"
                      placeholder="What would the ideal answer have been?"
                      rows="3"
                      class="mt-4 mb-1 w-full rounded-md dark:bg-gray-800 dark:focus:border-white dark:focus:ring-white"
                      tabindex="0"
                      style="height: 89.4815px; overflow-y: hidden"
                    ></textarea>
                  </form>
                  <div
                    class="mt-5 flex flex-col gap-3 sm:mt-4 sm:flex-row-reverse"
                  >
                    <button class="btn flex justify-center gap-2 btn-neutral">
                      Submit feedback
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <button
          type="button"
          aria-hidden="true"
          style="
            position: fixed;
            top: 1px;
            left: 1px;
            width: 1px;
            height: 0px;
            padding: 0px;
            margin: -1px;
            overflow: hidden;
            clip: rect(0px, 0px, 0px, 0px);
            white-space: nowrap;
            border-width: 0px;
          "
        ></button>
      </div>
    </div>

</div>
</template>

<script>
import { marked } from "marked";
import hljs from "highlight.js";
import "./assets/index.css";
import "highlight.js/styles/github.css";
document.title = "ChatGLM";
const Http = new XMLHttpRequest();
const url = process.env.VUE_APP_API+"/api/delete";
Http.open("POST", url);
Http.send();
Http.onreadystatechange = (e) => {
  if (Http.readyState === 4) {
    if (Http.status === 200) {
    }
        }
      };
const renderer = {
  code(code, infostring, escaped) {
    var codeHtml = code;
    if (infostring && infostring == "html") {
      codeHtml = encodeURIComponent(code);
    }
    if (infostring) {
      codeHtml = hljs.highlightAuto(code).value;
    }

    console.log(code, infostring, escaped, codeHtml);

    return `<div class="bg-black mb-4 rounded-md">
      <div class="code_header flex items-center relative text-gray-200 bg-gray-800 px-4 py-2 text-xs font-sans">
        <span>${infostring || ""}</span>
        <button onclick="copy(this)" class="flex ml-auto gap-2">
          <svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg">
            <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect>
          </svg>
          <span>Copy code</span>
          <code style="display:none">${encodeURIComponent(code)}</code>
        </button>
      </div>
      <div class="p-4 overflow-y-auto">
        <code class="!whitespace-pre hljs language-${infostring}">${codeHtml}</code>
      </div>
    </div>`;
  },
  paragraph(text) {
    return `<p style="white-space:pre-wrap;">${text}</p>`;
  },
};
marked.use({ renderer });

export default {
  data() {
    return {
      theme: "light",
      popupShow: true,
      avatarIdx: 1,
      conversations: [],
      conversation: [],
      chatMsg: "",
      chatTitle: "新的对话",
      convLoading: false,
      showSlide: false,
      isShowGoBottom: false,
      oldConv: undefined,
      convTitletmp: "",
      source: undefined,
      rsource: undefined,
      tsource: undefined,
      moreBar: false,
      enableWeather: false,
      enableDate: false,
      enableWeb: false,
      enableMarkmap: false,
      enableFiles: false,
      enableStableDiffusion: false
    };
  },
  methods: {
    switchButton(type) {
      const Http = new XMLHttpRequest();
      if (type == "web") {
        this.enableWeb = !this.enableWeb;
      } else if (type == "sd") {
        this.enableStableDiffusion = !this.enableStableDiffusion;
      } else if (type == "markmap") {
        this.enableMarkmap = !this.enableMarkmap;
      } else if (type == "weather") {
        this.enableWeather = !this.enableWeather;
      } else if (type == "date") {
        this.enableDate = !this.enableDate;
      }
      const url = process.env.VUE_APP_API+"/api/config?web="+this.enableWeb+"&sd="+this.enableStableDiffusion+"&markmap="+this.enableMarkmap+"&weather="+this.enableWeather+"&date="+this.enableDate;
      Http.open("POST", url);
      Http.send();
      Http.onreadystatechange = (e) => {
        if (Http.readyState === 4) {
          if (Http.status === 200) {
          }
        }
      };
    },
    sync_config(){
      const Http = new XMLHttpRequest();
      const url = process.env.VUE_APP_API+"/api/sync";
      Http.open("GET", url);
      Http.send();
      Http.onreadystatechange = (e) => {
        if (Http.readyState === 4) {
          if (Http.status === 200) {
            var content = Http.responseText
            var cfgJson = eval("(" + content + ")");
            //console.log(cfgJson)
            this.enableWeb = cfgJson['web']
            this.enableDate = cfgJson['date']
            this.enableWeather = cfgJson['weather']
            this.enableMarkmap = cfgJson['markmap']
            this.enableStableDiffusion = cfgJson['sd']
          }
        }
      };
    },
    closeSource() {
      var that = this;
      if (that.source) {
        that.source.close();
        that.source = undefined;
      }
      if (that.tsource) {
        that.tsource.close();
        that.tsource = undefined;
      }
      if (that.rsource) {
        that.rsource.close();
        that.rsource = undefined;
      }
    },
    suitable() {},
    copy(idx, conv) {
      var content = conv['speeches'][0];
      const authentication = () => {
      if ("clipboard" in navigator) {
        return new Promise((resolve, reject) => {
          navigator.permissions.query({ name: "clipboard-read" }).then(
            (result) => {
              if (result.state == "granted" || result.state == "prompt") {
                resolve(true);
              } else {
                resolve(false);
              }
            },
            (error) => {
              reject(error);
            }
          );
        });
      } else {
        return Promise.resolve(false);
      }
    };
      navigator.clipboard.writeText(content.trim())
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      const formData = new FormData();
      //this.inputChat('[File]'+file['name']+" ")
      formData.append('file', file);
      fetch(process.env.VUE_APP_API+"/api/upload", {
        method: 'POST',
        body: formData
      })
    },
    stopChat() {
      var that = this;
      this.axios
        .post(process.env.VUE_APP_API+"/api/stop/", {})
        .then((result) => {
          var rconv = that.conversation[that.conversation.length - 1];
          rconv["loading"] = false;
          that.convLoading = false;

          if (that.conversation.length == 2 && rconv["speeches"].length == 1) {
            var newConv = {
              id: that.cid,
              title: "新的对话",
            };

            that.generateConvTitle(newConv);
            that.conversations.unshift(newConv);
            that.selectConversation(newConv, false);
            that.saveConversations();
          }

          that.refreshConversation();
          that.closeSource();
        })
        .catch((err) => {
          that.closeSource();
        });
    },
    closeShowSlide() {
      this.showSlide = false;
      this.$refs.menu.appendChild(this.$refs.navEle);
    },
    showSlideMethod() {
      this.showSlide = true;
      this.$refs.slideNavContainer.appendChild(this.$refs.navEle);
    },
    moreBarShow() {
      this.sync_config();
      this.moreBar = true;
    },
    moreBarClose() {
      this.moreBar = false;
    },
    changeHeight() {
      var elem = this.$refs.inputChat;
      elem.style.height = "24px";
      var scrollHeight = elem.scrollHeight;
      if (24 >= scrollHeight || this.chatMsg.length == 0) {
        this.resetHeight();
        return;
      }

      elem.style.removeProperty("overflow-y");
      elem.style.height = scrollHeight + "px";
    },
    resetHeight() {
      var elem = this.$refs.inputChat;
      elem.style.height = "24px";
      elem.style["overflow-y"] = "hidden";
    },
    closePopup() {
      this.popupShow = false;
    },
    vueCopy(node) {
      var code = node.getElementsByTagName("code")[0].innerHTML;
      var text = decodeURIComponent(code);
      this.$copyText(text).then(
        (res) => {
          var svg = `<svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg">
                        <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                    <span>Copied!</span>`;
          const nodeInnerHtml = node.innerHTML;
          node.innerHTML = svg;

          setTimeout(() => {
            node.innerHTML = nodeInnerHtml;
          }, 1000);
        },
      );
    },
    changeTheme(theme) {
      this.theme = theme;
      var html = document.getElementsByTagName("html")[0];
      html.classList.remove("light", "dark");
      html.classList.add(theme);
      html.style["color-scheme"] = theme;
      localStorage.setItem("theme", theme);
    },
    initConvs(convs) {
      for (let i = 0; i < convs.length; i++) {
        var conv = convs[i];
        if (conv.speaker == "human") {
          continue;
        }
        conv["idx"] = conv["speeches"].length - 1;
      }
      return convs;
    },
    last(conv) {
      if (conv.idx == 0) {
        return;
      }
      conv.idx--;
      this.refreshConversation();
    },
    next(conv) {
      if (conv.idx == conv["speeches"].length - 1) {
        return;
      }
      conv.idx++;
      this.refreshConversation();
    },
    inputChat(msg) {
      this.chatMsg = msg;
    },
    countAndConcat(str, substr) {
      const matches = str.match(new RegExp(substr, "g"));
      const count = matches ? matches.length : 0;
      const isOdd = count % 2 === 1;
      return isOdd ? str + "\n" + substr : str;
    },
    mdToHtml(md, conv) {
      if (md == "") {
        return "<p></p>";
      }

      md = this.countAndConcat(md, "```");

      var htmlMD = marked.parse(md);
      htmlMD = htmlMD.trim();
      return htmlMD;
    },
    refreshConversation() {
      this.conversation = JSON.parse(JSON.stringify(this.conversation));
    },
    chatRepeat() {
      if (this.convLoading) {
        return;
      }
      var that = this;
      const Http = new XMLHttpRequest();
      const url = process.env.VUE_APP_API+"/api/repeat";
      Http.open("GET", url);
      Http.send();
      Http.onreadystatechange = (e) => {
        if (Http.readyState === 4) {
          if (Http.status === 200) {
            var content = Http.responseText;
            var rconv = that.conversation[that.conversation.length - 1];
            rconv["loading"] = false;
            that.convLoading = false;
            var idx = rconv.idx;
            that.handleScrollBottom();
            rconv["speeches"][idx] += content;
            that.refreshConversation();
            that.rsource = undefined;
            return;
          }
        }
      };
    },
    judgeInput(e) {
      if (!e.shiftKey && e.keyCode == 13) {
        e.cancelBubble = true;
        e.stopPropagation();
        e.preventDefault();
        this.send();
      }
    },
    send() {
    if (this.chatMsg.trim().length == 0) {
      return;
    }

    if (this.convLoading) {
      return;
    }

    this.convLoading = true;
    var chatMsg = this.chatMsg;
    chatMsg = chatMsg.trim().replace(/\n/g, "");
    this.chatMsg = "";

    var first = this.conversation.length == 0;

    this.conversation.push({
      speaker: "human",
      speech: chatMsg,
    });

    var conv = {
      idx: 0,
      loading: true,
      speaker: "ai",
      suitable: [0],
      speeches: [""],
    };
    this.conversation.push(conv);

    this.handleScrollBottom();

    var that = this;
    var source = (this.source = new EventSource(process.env.VUE_APP_API+"/api/chat?prompt=" + encodeURIComponent(chatMsg)));

    source.addEventListener("open", function () {
    });

    source.addEventListener("message", function (e) {
      var conv = that.conversation[that.conversation.length - 1];
      if (e.data == "[DONE]") {
        source.close();
        conv["loading"] = false;
        that.convLoading = false;

        if (first) {
          var newConv = {
            id: that.cid,
            title: "新的对话",
          };

          that.generateConvTitle(newConv);
          that.conversations.unshift(newConv);
          that.selectConversation(newConv, false);
          that.saveConversations();
        }
        that.refreshConversation();
        that.source = undefined;
        return;
      }

      var content = e.data;
      if (content.includes("[ENTRY]")) {
        content = content.replaceAll("[ENTRY]", "\n");
      }

      that.handleScrollBottom();

      conv["speeches"][0] = content;
      that.refreshConversation();
    });

    source.addEventListener("error", function (e) {
      var conv = that.conversation[that.conversation.length - 1];
      source.close();
        conv["loading"] = false;
        that.convLoading = false;
        if (first) {
          var newConv = {
            id: that.cid,
            title: "新的对话",
          };
          that.generateConvTitle(newConv);
          that.conversations.unshift(newConv);
          that.selectConversation(newConv, false);
          that.saveConversations();
        }
        that.refreshConversation();
        that.source = undefined;
        return;
    });
  },
    generateConvTitle(conv) {
      conv.title = ""
      var that = this;
      const Http = new XMLHttpRequest();
      const url = process.env.VUE_APP_API+"/api/title";
      Http.open("GET", url);
      Http.send();
      Http.onreadystatechange = (e) => {
        if (Http.readyState === 4) {
          if (Http.status === 200) {
            var content = Http.responseText;
            conv.title += content;
            that.selectConversation(conv, false);
            that.saveConversations();
            that.tsource = undefined;
            return;
          }
        }
      };
    },
    newChat() {
      this.conversations = [];
      this.saveConversations();
      if (this.conversation.length == 0) {
        return;
      }
      this.chatTitle = "新的对话";
      document.title = "新的对话";
      var conversations = this.conversations;
      for (let idx in conversations) {
        var conv = conversations[idx];
        delete conv.editable;
        delete conv.selected;
        delete conv.delete;
      }
      const Http = new XMLHttpRequest();
      const url = process.env.VUE_APP_API+"/api/delete";
      Http.open("POST", url);
      Http.send();
      Http.onreadystatechange = (e) => {
        if (Http.readyState === 4) {
          if (Http.status === 200) {
            var content = Http.responseText;
            var rconv = that.conversation[that.conversation.length - 1];
            rconv["loading"] = false;
            that.convLoading = false;
            var idx = rconv.idx;
            that.handleScrollBottom();
            rconv["speeches"][idx] += content;
            that.refreshConversation();
            that.rsource = undefined;
            return;
          }
        }
      };
    },
    loadConversations() {
      let convs = localStorage.getItem("conversations") || "[]";
      this.conversations = JSON.parse(convs);
    },
    saveConversations() {
      var conversations = JSON.parse(JSON.stringify(this.conversations));
      for (let idx in conversations) {
        var conv = conversations[idx];
        delete conv.editable;
        delete conv.selected;
        delete conv.delete;
      }
      let convs = JSON.stringify(conversations);
      localStorage.setItem("conversations", convs);
    },
    clearConversations() {
      this.conversations = [];
      this.saveConversations();
      document.location.reload();
    },
    selectConversation(conv, loadConv) {
      var that = this;
      if (this.oldConv) {
        this.oldConv.selected = false;
      }
      conv.selected = true;
      this.oldConv = conv;
      if (!loadConv) {
        return;
      }
    },
    editTitle(idx, conv) {
      this.convTitletmp = conv.title;
      conv.editable = true;
      this.$set(this.conversations, idx, conv);
      setTimeout(() => {
        document.getElementById("titleInput").focus();
      }, 150);
    },
    titleInputBlur(idx, conv) {
      setTimeout(() => {
        this.cancelChangeConvTitle(idx, conv);
      }, 100);
    },
    changeConvTitle(idx, conv) {
      conv.title = this.convTitletmp;
      this.saveConversations();
      this.cancelChangeConvTitle(idx, conv);
    },
    cancelChangeConvTitle(idx, conv) {
      conv.editable = false;
      this.$set(this.conversations, idx, conv);
    },
    delConv(cidx) {
      const Http = new XMLHttpRequest();
      const url = process.env.VUE_APP_API+"/api/delete";
      Http.open("POST", url);
      Http.send();
      Http.onreadystatechange = (e) => {
        if (Http.readyState === 4) {
          if (Http.status === 200) {
            var content = Http.responseText;
            var rconv = that.conversation[that.conversation.length - 1];
            rconv["loading"] = false;
            that.convLoading = false;
            var idx = rconv.idx;
            that.handleScrollBottom();
            rconv["speeches"][idx] += content;
            that.refreshConversation();
            that.rsource = undefined;
            return;
          }
        }
      };
      this.conversations.splice(cidx, 1);
      this.saveConversations();
    },
    cancelDelConv(idx, conv) {
      conv.delete = false;
      this.$set(this.conversations, idx, conv);
    },
    loadAvatar() {
      let avatar =
        localStorage.getItem("avatar") || Math.ceil(Math.random() * 9);
      this.avatarIdx = avatar;
    },
    handleScrollBottom() {
      this.$nextTick(() => {
        let scrollElem = this.$refs.chatContainer;
        scrollElem.scrollTo({
          top: scrollElem.scrollHeight,
          behavior: "smooth",
        });
      });
    },
    isScrollAndNotBottom() {
      let chatDivEle = this.$refs.chatContainer;
      if (!chatDivEle) {
        return;
      }

      if (chatDivEle.scrollHeight <= chatDivEle.clientHeight) {
        this.isShowGoBottom = false;
        return;
      }

      const scrollTop = chatDivEle.scrollTop;
      const windowHeight = chatDivEle.clientHeight;
      const scrollHeight = chatDivEle.scrollHeight;
      if (scrollTop + windowHeight >= scrollHeight - 50) {
        this.isShowGoBottom = false;
        return;
      }

      this.isShowGoBottom = true;
    },
  },
  computed: {},
  watch: {
    chatMsg(newVal, oldVal) {
      if (newVal === oldVal) {
        return;
      }
      this.changeHeight();
    },
  },
  mounted: function () {
    var theme = localStorage.getItem("theme") || "light";
    this.changeTheme(theme);
    this.loadConversations();
    this.loadAvatar();

    let chatDivEle = this.$refs.chatContainer;
    chatDivEle.addEventListener("scroll", this.isScrollAndNotBottom, true);
    window.copy = this.vueCopy;
  },
};
  import "./assets/style/style.css"
  import "./assets/style/switch.css";
</script>
