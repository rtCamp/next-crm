import { createResource } from "frappe-ui"
import { employeeResource } from "./employee"
import dayjs from "@/utils/dayjs"

const transformLeaveData = (data) => {
	return data.map((leave) => {
		leave.leave_dates = getLeaveDates(leave)
		leave.doctype = "Leave Application"
		return leave
	})
}

export const getLeaveDates = (leave) => {
	if (leave.from_date == leave.to_date)
		return dayjs(leave.from_date).format("D MMM")
	else
		return `${dayjs(leave.from_date).format("D MMM")} - ${dayjs(
			leave.to_date
		).format("D MMM")}`
}

// Ensure employee data is available before accessing its properties
const getEmployeeName = () => employeeResource?.data?.name || "unknown"
const getEmployeeUserID = () => employeeResource?.data?.user_id || "unknown"

export const myLeaves = createResource({
	url: "shop.api.get_leave_applications",
	params: {
		employee: getEmployeeName(),
		limit: 5,
	},
	auto: true,
	cache: "shop:my_leaves",
	transform(data) {
		return transformLeaveData(data)
	},
	onSuccess() {
		leaveBalance.reload()
	},
})

export const teamLeaves = createResource({
	url: "shop.api.get_leave_applications",
	params: {
		employee: getEmployeeName(),
		approver_id: getEmployeeUserID(),
		for_approval: 1,
		limit: 5,
	},
	auto: true,
	cache: "shop:team_leaves",
	transform(data) {
		return transformLeaveData(data)
	},
})

export const leaveBalance = createResource({
	url: "shop.api.get_leave_balance_map",
	params: {
		employee: getEmployeeName(),
	},
	auto: true,
	cache: "shop:leave_balance",
	transform: (data) => {
		// Calculate balance percentage for each leave type
		return Object.fromEntries(
			Object.entries(data).map(([leave_type, allocation]) => {
				allocation.balance_percentage =
					(allocation.balance_leaves / allocation.allocated_leaves) * 100
				return [leave_type, allocation]
			})
		)
	},
})
