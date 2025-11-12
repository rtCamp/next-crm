import { getRandomString } from "./stringUtils.js";

/**
 * Generates random lead data for testing
 * @returns {Object} Lead data with randomized values
 */
export const generateLeadData = () => {
  const timestamp = Date.now();
  const randomStr = getRandomString(5);

  return {
    salutation: "Mr",
    first_name: `TC-LL-2-FN-${randomStr}`,
    last_name: `LN-${timestamp}`,
    company_name: `Playwright test Co -  ${randomStr}`,
    email_id: `john.TC-LL-2-${randomStr}@gmail.com`,
    mobile_no: `+91 ${Math.floor(Math.random() * 9000000000) + 1000000000}`,
    gender: "Male",
    annual_revenue: String(Math.floor(Math.random() * 900000) + 100000),
    status: "New",
  };
};
