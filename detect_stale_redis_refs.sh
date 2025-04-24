#!/bin/bash

# Fetch all Helm releases across all namespaces
releases=$(helm list --all-namespaces -q)

# Initialize a flag to track if any stale references are found
found_stale=false

# Iterate over each release to inspect its manifest
for release in $releases; do
  # Extract the namespace of the current release
  namespace=$(helm list --all-namespaces | grep "^$release\s" | awk '{print $2}')
  
  # Retrieve the manifest of the current release
  manifest=$(helm get manifest "$release" -n "$namespace")
  
  # Check for references to 'redis-config' in the manifest
  if echo "$manifest" | grep -q 'redis-config'; then
    echo "Stale reference found in release: $release (Namespace: $namespace)"
    found_stale=true
  fi
done

# Provide feedback based on the findings
if [ "$found_stale" = false ]; then
  echo "No stale references to 'redis-config' found in any Helm release."
fi

