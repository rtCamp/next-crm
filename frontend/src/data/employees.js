import { createResource } from "frappe-ui"
import { reactive } from "vue"

let employeesByID = reactive({})
let employeesByUserID = reactive({})

export const employees = createResource({
    url: "shop.api.get_all_employees",
    auto: true,
    transform(data) {
        return data.map((employee) => {
            employee.isActive = employee.status === "Active"
            employeesByID[employee.name] = employee
            employeesByUserID[employee.user_id] = employee
            return employee
        })
    },
    onError(error) {
        if (error && error.exc_type === "AuthenticationError") {
            router.push({ name: "Login" })
        }
    },
})

export function getEmployeeInfo(employeeID) {
    return employeesByID[employeeID] || null
}

export function getEmployeeInfoByUserID(userID) {
    return employeesByUserID[userID] || null
}
