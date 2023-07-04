const accessToken = '3796899bd37c423bad3a21a25277bce0'
const baseUrl = 'snd_msg_to_bot/'
const sessionId = '20150910';
const loader = `<span class='loader'><span class='loader__dot'></span><span class='loader__dot'></span><span class='loader__dot'></span></span>`
const errorMessage = 'My apologies, I\'m not available at the moment, however, feel free to reach out our amadeus support team.'
const urlPattern = /(\b(https?|ftp):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/gim
const chatbot = document.querySelector('.chatbot')
const chatbotMessageWindow = document.querySelector('.chatbot__message-window')
const chatbotHeader = document.querySelector('.chatbot__header')
const chatbotMessages = document.querySelector('.chatbot__messages')
const chatbotInput = document.querySelector('.chatbot__input')
const chatbotSubmit = document.querySelector('.chatbot__submit')
const chatbot_icon = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAACXBIWXMAAAsTAAALEwEAmpwYAAAD0UlEQVR4nOWVTVAbZRjHoxd17EkPOl48qOPoTUdnenHGgycveu5Rp4zTGcepkJZmSrJpCxLSDUl2F8JHA5uFZPNuQspHCoVkYgj5ogQhDU0hSekQSKSAmCgarPo4u5g0ZYAEhFx8Zv6HPez/N//3fZ7nFYmOUPh59IJCzLyPn+94SVSpwiXMaUqOkqjDvdbWYEsTUss3FQGTchSdC61BfC4L8UgW2hpsP1Ykua6+b1mA/is+OX/sJw6mMOQOuhb/5qF88ha5ZUkm63r+xMHqS8ZXeHjrVWuOknNz6lrmQ1ElS1nT/X1Fgf8PsOZrzXOqi/RnFIYGKTkX19X3Lemu9eX4Dm+9wiUojPOpJL1VxzZWIIJnmiXGL0gZWhpgAtnpieXCGBUrcmcVRi0zudar1jRx2axQVhtePDKUlKFTmjrW2aefyMzPbu4J3K1YJANOWzinrWNjTTXdb5QFuv4t/V5+HnmoVsrOue33/ygHuFs/eFeAwlBKWc28u5d/oVQSU5VeObhBStl+mUz2rKaOdY3b7+eOAs1rNpAGQmp+2FBLv1zs/4S6k1AdcCaAxFBUIzFV3aS9mf8Czcs3FvuTkJptxf77gecpDCXLvdNypMeH1kgpyxwIJmRoeag3mM3/tBDeBPetKIxwIbhtKU+ugYiww/MeQdciEJg5WirxrzO+1M6ITD0Cg9oOk64ILM6vwMOFVFkKT8aB0d4SgPlOJzD0y8GJMVToYq7DBenkOmw//gsSKxkop1LrW5DZ2obc79tANw9B7G5G8Gqrt24dnFiOHufBPcSwYNZomoGvNH4YnUqWhJ5VeeCcekL4vs35Ydq7s3BuNA3+VgLMPQFrd8BGRwy+VLohnNg4EMwnPaf2gIyeEr4HezwQDq4KXt2q4VzZ4CHjJMwG5uEo9Sj1E/QSI4UGOxR44e7PYNV7ALU7wDMyAz5HuKS8Y7NCUh4amVwtDSakJoXbHn3qjvO6N70OAecD8I3FS8rviBeOt1jduD0n+GMo/BQYrzW8SUhZD3XFsnlci6NYls7xjFbKhpsvs5+L9ipdvS19EuB+g39TWd318Z5Q4cgxczI0kTxWKL/F2hv71xVi5u19wcrqntdJjBtt/+5mqt/gz/qdCeGODwPi9/yd8SUYZkM5/XV7msK4sOoS89G+0F1dfkohpj8lMESQGPJSGIrrrllX9Lg9bWxxpC2d42sDTHDDesOzYaIcq3TzcLq9wZZqkXMPKAyFSDli8Is9Z5pqul4tC1iq+LdVIda/pRDTHzTV0J/gF7pON16g31GIO1/j3/HDmP0Dsy+Ll+KuL0wAAAAASUVORK5CYII="

const botLoadingDelay = 1000
const botReplyDelay = 2000

document.addEventListener('keypress', event => {
    if (event.which == 13) validateMessage()
}, false)

chatbotHeader.addEventListener('click', () => {
    toggle(chatbot, 'chatbot--closed')
    chatbotInput.focus()
}, false)

chatbotSubmit.addEventListener('click', () => {
    validateMessage()
}, false)

const toggle = (element, klass) => {
    const classes = element.className.match(/\S+/g) || [],
        index = classes.indexOf(klass)
    index >= 0 ? classes.splice(index, 1) : classes.push(klass)
    element.className = classes.join(' ')
}

const userMessage = content => {
    chatbotMessages.innerHTML += `<li class='is-user animation'>
      <p class='chatbot__message'>
        ${content}
      </p>
      <span class='chatbot__arrow chatbot__arrow--right'></span>
    </li>`
}

const aiMessage = (content, isLoading = false, delay = 0) => {
    setTimeout(() => {
        removeLoader()
        chatbotMessages.innerHTML += `<li 
      class='is-ai animation' 
      id='${isLoading ? "is-loading" : ""}'>
        <div class="is-ai__profile-picture">
        <img src=${chatbot_icon}>
        </div>
        <span class='chatbot__arrow chatbot__arrow--left'></span>
        <div class='chatbot__message'>${content}</div>
      </li>`
        scrollDown()
    }, delay)
}

const removeLoader = () => {
    let loadingElem = document.getElementById('is-loading')
    if (loadingElem) chatbotMessages.removeChild(loadingElem)
}

const escapeScript = unsafe => {
    const safeString = unsafe
        .replace(/</g, ' ')
        .replace(/>/g, ' ')
        .replace(/&/g, ' ')
        .replace(/"/g, ' ')
        .replace(/\\/, ' ')
        .replace(/\s+/g, ' ')
    return safeString.trim()
}

const linkify = inputText => {
    return inputText.replace(urlPattern, `<a href='$1' target='_blank'>$1</a>`)
}

const validateMessage = () => {
    const text = chatbotInput.value
    const safeText = text ? escapeScript(text) : ''
    if (safeText.length && safeText !== ' ') {
        resetInputField()
        userMessage(safeText)
        send(safeText)
    }
    scrollDown()
    return
}

const multiChoiceAnswer = text => {
    const decodedText = text.replace(/zzz/g, "'")
    userMessage(decodedText)
    send(decodedText)
    scrollDown()
    return
}

const processResponse = val => {
    if (val && val.fulfillment) {
        let output = ''
        let messagesLength = val.fulfillment.messages.length
        for (let i = 0; i < messagesLength; i++) {
            let message = val.fulfillment.messages[i]
            let type = message.type

            switch (type) {
                // 0 fulfillment is text
                case 0:
                    let parsedText = linkify(message.speech)
                    output += `<p>${parsedText}</p>`
                    break

                // 1 fulfillment is card
                case 1:
                    let imageUrl = message.imageUrl
                    let imageTitle = message.title
                    let imageSubtitle = message.subtitle
                    let button = message.buttons[0]

                    if (!imageUrl && !button && !imageTitle && !imageSubtitle) break

                    output += `
            <a class='card' href='${button.postback}' target='_blank'>
              <img src='${imageUrl}' alt='${imageTitle}' />
            <div class='card-content'>
              <h4 class='card-title'>${imageTitle}</h4>
              <p class='card-title'>${imageSubtitle}</p>
              <span class='card-button'>${button.text}</span>
            </div>
            </a>
          `
                    break

                // 2 fulfillment is a quick reply with multi-choice buttons
                case 2:
                    let title = message.title
                    let replies = message.replies
                    let repliesLength = replies.length
                    output += `<p>${title}</p>`

                    for (let i = 0; i < repliesLength; i++) {
                        let reply = replies[i]
                        let encodedText = reply.replace(/'/g, 'zzz')
                        output += `<button onclick='multiChoiceAnswer("${encodedText}")'>${reply}</button>`
                    }
                    break
            }
        }

        removeLoader()
        return output
    }
    else if (!!val && val.indexOf('DOCTYPE') === -1) {
        let parsedText = linkify(val)
        let output = `<p>${parsedText}</p>`
        removeLoader()
        return output
    }

    removeLoader()
    return `<p>${errorMessage}</p>`
}

const setResponse = (val, delay = 0) => {
    setTimeout(() => {
        aiMessage(processResponse(val))
    }, delay)
}

const resetInputField = () => {
    chatbotInput.value = ''
}

const scrollDown = () => {
    const distanceToScroll =
        chatbotMessageWindow.scrollHeight -
        (chatbotMessages.lastChild.offsetHeight + 60)
    chatbotMessageWindow.scrollTop = distanceToScroll
    return false
}

const send = (text = '') => {
    fetch(`${baseUrl}?message=${text}&session=${localStorage.api_key}`, {
        method: 'GET',
        dataType: 'json',
        headers: {
            Authorization: 'Bearer ' + accessToken,
            'Content-Type': 'application/json; charset=utf-8'
        }
    })
        .then(response => response.text())
        .then(res => {
            if (res.status < 200 || res.status >= 300) {
                let error = new Error(res.statusText)
                throw error
            }
            return res
        })
        .then(res => {
            setResponse(res, botLoadingDelay + botReplyDelay)
        })
        .catch(error => {
            setResponse(errorMessage, botLoadingDelay + botReplyDelay)
            resetInputField()
            console.log(error)
        })

    aiMessage(loader, true, botLoadingDelay)
}

function logout() {
    window.location.href = '../logout/'
}

function prototype(path) {
    const form = document.createElement('form')
    form.method = 'post'
    form.action = path
    form.target = "_blank"
    const hiddenField = document.createElement('input')
    hiddenField.type = 'hidden'
    hiddenField.name = "csrfmiddlewaretoken"
    hiddenField.value = document.getElementsByName('csrfmiddlewaretoken')[0].value
    form.appendChild(hiddenField)
    document.body.appendChild(form)
    form.submit()
}
