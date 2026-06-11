const states = ["loading", "empty", "error", "success"];

if (states.length !== 4) {
  throw new Error("frontend fixture state matrix is incomplete");
}

