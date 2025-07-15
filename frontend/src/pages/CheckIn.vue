<template>
	<div id="checkInDiv" class="flex flex-col items-center bg-white h-full rounded w-full py-6 px-4 border-none gap-4">
		<!-- CAMERA / SELFIE SECTION -->
		<div class="w-full flex flex-col items-center gap-2">
			<video id="img" ref="videoRef" autoplay playsinline class="object-cover border" v-show="!capturedImage" />
			<img :src="capturedImage" id="capture" class="object-cover border" v-if="capturedImage" />
			<canvas ref="canvasRef" class="hidden"></canvas>
			<!-- <Button v-if="!capturedImage" variant="outline" size="sm" class="text-xs" @click="capturePhoto">
				📸 Capture Selfie
			</Button> -->
		</div>

		<!-- Map Section -->
		<div class="flex flex-col gap-1.5 mt-2 items-center justify-center">
			<div class="font-bold text-xl">{{ dayjs(checkinTimestamp).format("hh:mm:ss a") }}</div>
			<div class="font-medium text-gray-500 text-sm">{{ dayjs().format("D MMM, YYYY") }}</div>
		</div>

		<template v-if="settings.data?.allow_geolocation_tracking">
			<span v-if="locationStatus" class="font-medium text-gray-500 text-sm">
				{{ locationStatus }}
			</span>
			<div class="rounded border-4  w-full h-170">
				<iframe
					width="100%"
					
					frameborder="0"
					scrolling="no"
					marginheight="0"
					marginwidth="0"
					style="border: 0"
					:src="`https://maps.google.com/maps?q=${latitude},${longitude}&hl=en&z=15&amp;output=embed`"
				></iframe>
			</div>
		</template>

		<!-- User Info -->
		<div class="text-xs text-left w-full font-medium text-gray-800">
			<p><strong>Date:</strong> {{ dayjs().format("DD-MM-YYYY") }}</p>
			<p><strong>User ID:</strong> {{ CheckEmployee.user_id }}</p>
			<p><strong>Employee:</strong> {{ CheckEmployee.name }}</p>
			<p><strong>Employee Name:</strong> {{ CheckEmployee.employee_name }}</p>
		</div>

		<!-- Buttons -->
		<div class="flex flex-col gap-2 w-full mt-2">
			<Button variant="solid" class="w-full py-3 text-sm" @click="submitLog(nextAction.action)">
				{{ nextAction.label }}
			</Button>
			<router-link :to="{ name: 'EmployeeCheckinListView' }" class="w-full">
				<Button variant="outline" class="w-full py-3 text-sm">
					{{ __("Attendance List") }}
				</Button>
			</router-link>
		</div>
	</div>
</template>
  
  
<script setup>
import { createResource, createListResource, toast, FeatherIcon, Button } from "frappe-ui"
import { computed, inject, ref, onMounted, onBeforeUnmount, provide } from "vue"
import { IonModal, modalController } from "@ionic/vue"
import { formatTimestamp } from "@/utils/formatters"
import axios from 'axios'


onBeforeUnmount(() => {
	socket.emit("doctype_unsubscribe", DOCTYPE)
	socket.off("list_update")

	if (videoRef.value?.srcObject) {
		videoRef.value.srcObject.getTracks().forEach(track => track.stop())
		videoRef.value.srcObject = null
	}
})


const DOCTYPE = "Employee Checkin"
const socket = inject("$socket")

const employee = ref(null)
const CheckEmployee = ref([])
onMounted(async () => {
  try {
    const session = await axios.get('/api/method/frappe.auth.get_logged_user')
    const user = session?.data?.message
    console.log("Logged-in user:", user)

    if (user) {
      const response = await axios.get('/api/resource/Employee', {
        params: {
          fields: JSON.stringify(['*']),  // Get all fields
          filters: JSON.stringify([['user_id', '=', user]])
        }
      })

      const empData = response?.data?.data?.[0]  // Get the first matching employee
      if (empData) {
        employee.value = empData
        CheckEmployee.value = empData
        console.log("Matched Employee:", empData)
      } else {
        console.warn("No employee found for user:", user)
      }
    }
  } catch (err) {
    console.error('Failed to fetch employee:', err)
  }
})

const dayjs = inject("$dayjs")
const __ = inject("$translate", (key, params = []) =>
	key.replace(/\{(\d+)\}/g, (_, index) => params[+index])
)

const checkinTimestamp = ref(null)
const latitude = ref(null)
const longitude = ref(null)
const locationStatus = ref("")
const session = inject("$session")
const user = inject("$user")

const settings = createResource({
	url: "next_crm.api.api.get_hr_settings",
	auto: true,
})

const checkins = createListResource({
	doctype: DOCTYPE,
	fields: ["employee", "employee_name", "log_type", "time", "device_id"],
	filters: { employee: CheckEmployee.value.name },
	orderBy: "time desc",
})
checkins.reload()

const lastLog = computed(() => checkins.list.loading || !checkins.data ? {} : checkins.data[0])
const lastLogType = computed(() => lastLog?.value?.log_type === "IN" ? "check-in" : "check-out")
const nextAction = computed(() => lastLog?.value?.log_type === "IN"
	? { action: "OUT", label: __("Check Out") }
	: { action: "IN", label: __("Mark Attendance") }
)

// ✅ Updated Geolocation Logic
function handleLocationSuccess(position) {
	latitude.value = position.coords.latitude
	longitude.value = position.coords.longitude

	locationStatus.value = [
		__("Latitude: {0}°", [Number(latitude.value).toFixed(5)]),
		__("Longitude: {0}°", [Number(longitude.value).toFixed(5)])
	].join(", ")
}

function handleLocationError(error) {
	locationStatus.value = `Location Error: (${error.code}) ${error.message || ''}`
}

const fetchLocation = () => {
	return new Promise((resolve, reject) => {
		if (!navigator.geolocation) {
			locationStatus.value = __("Geolocation is not supported by your browser.")
			return reject("Not supported")
		}
		locationStatus.value = __("Locating...")
		navigator.geolocation.getCurrentPosition(
			(position) => {
				latitude.value = position.coords.latitude
				longitude.value = position.coords.longitude
				locationStatus.value = `Latitude: ${latitude.value}, Longitude: ${longitude.value}`
				resolve()
			},
			(error) => {
				locationStatus.value = `Location Error: (${error.code}) ${error.message || ''}`
				reject(error)
			},
			{ enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
		)
	})
}

 fetchLocation()

const handleEmployeeCheckin = () => {
	checkinTimestamp.value = dayjs().format("YYYY-MM-DD HH:mm:ss")
	if (settings.data?.allow_geolocation_tracking) {
		fetchLocation()
	}
}
handleEmployeeCheckin()

const submitLog = async (logType) => {
	const actionLabel = logType === "IN" ? __("Check-in") : __("Check-out")

	if (settings.data?.allow_geolocation_tracking) {
		try {
			await fetchLocation()
		} catch (err) {
			toast({
				title: __("Location Error"),
				text: __("Unable to get location. Please enable location services."),
				icon: "alert-circle",
				position: "bottom-center",
				iconClasses: "text-yellow-500",
			})
			return
		}
	}

	if (!employee?.value?.name) {
		toast({
			title: __("Error"),
			text: __("Employee not found. Please try again."),
			icon: "alert-circle",
			position: "bottom-center",
			iconClasses: "text-red-500",
		})
		return
	}

	// 🔸 Auto-capture selfie before submission
	await capturePhoto()

	checkins.insert.submit({
		employee: CheckEmployee.value.name,
		log_type: logType,
		time: checkinTimestamp.value,
		latitude: latitude.value,
		longitude: longitude.value,
	}, {
		onSuccess: async (doc) => {
			// 🔸 Upload captured selfie
			if (capturedImage.value) {
				await uploadSelfieToCheckin(doc.name)
			}

			modalController.dismiss()
			toast({
				title: __("Success"),
				text: __("{0} successful!", [actionLabel]),
				icon: "check-circle",
				position: "bottom-center",
				iconClasses: "text-green-500",
			})

			window.location.reload()
		},
		onError(error) {
			console.error("Check-in failed", error)
			toast({
				title: __("Error"),
				text: __("{0} failed!", [actionLabel]),
				icon: "alert-circle",
				position: "bottom-center",
				iconClasses: "text-red-500",
			})

			window.location.reload()
		},
	})
}




onMounted(() => {
	socket.emit("doctype_subscribe", DOCTYPE)
	socket.on("list_update", (data) => {
		if (data.doctype === DOCTYPE) checkins.reload()
	})
	startCamera()
})

onBeforeUnmount(() => {
	socket.emit("doctype_unsubscribe", DOCTYPE)
	socket.off("list_update")
})

// 🟡 Camera / Selfie
const videoRef = ref(null)
const canvasRef = ref(null)
const capturedImage = ref(null)

const startCamera = async () => {
	try {
		const stream = await navigator.mediaDevices.getUserMedia({ video: true })
		if (videoRef.value) videoRef.value.srcObject = stream
	} catch (err) {
		console.error("Camera error:", err)
	}
}

const capturePhoto = async () => {
	const video = videoRef.value
	const canvas = canvasRef.value
	if (!video || !canvas) return

	canvas.width = video.videoWidth
	canvas.height = video.videoHeight
	const context = canvas.getContext("2d")
	context.drawImage(video, 0, 0, canvas.width, canvas.height)

	canvas.toBlob(async (blob) => {
		const file = new File([blob], "selfie.jpg", { type: "image/jpeg" })
		capturedImage.value = URL.createObjectURL(file)

	}, "image/jpeg", 0.9)

}

const uploadSelfieToCheckin = async (docname) => {
	const blob = await fetch(capturedImage.value).then(res => res.blob())
	const file = new File([blob], "selfie.jpg", { type: "image/jpeg" })

	const formData = new FormData()
	formData.append("file", file)
	formData.append("is_private", "0")
	formData.append("doctype", "Employee Checkin")
	formData.append("fieldname", "image")
	formData.append("docname", docname) // ✅ actual check-in document name

	try {
		await axios.post("/api/method/upload_file", formData, {
			headers: { "Content-Type": "multipart/form-data" }
		})
		console.log("Selfie uploaded for", docname)
	} catch (err) {
		console.error("Failed to upload selfie:", err)
		toast({
			title: __("Upload Error"),
			text: __("Failed to upload selfie."),
			icon: "alert-circle",
			position: "bottom-center",
			iconClasses: "text-red-500",
		})
	}
}

</script>
  
  <style>
  
  
  
  
  
  
  
  #img{
	  border-radius: 10%;
	  height: 84%;
  }
  #capture{
	  border-radius: 10%;
	  height: 84%;
  }
   
  </style>