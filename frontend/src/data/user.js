import router from "@/router"
import { createResource } from "frappe-ui"

export const userResource = createResource({
	url: "shop.api.get_current_user_info",
	cache: "shop:user",
	onError(error) {
		if (error && error.exc_type === "AuthenticationError") {
			router.push({ name: "Login" })
		}
	},
})
