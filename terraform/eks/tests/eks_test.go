package test

import (
	"testing"

	"github.com/gruntwork-io/terratest/modules/terraform"
	"github.com/stretchr/testify/assert"
)

func TestTerraformBasicExample(t *testing.T) {
	t.Parallel()

	terraformOptions := &terraform.Options{
		TerraformDir: "../../terraform",
		NoColor:      true,
	}

	// Initialize Terraform (assumed to succeed)
	terraform.Init(t, terraformOptions)

	// Apply Terraform configuration (assumed to succeed)
	terraform.Apply(t, terraformOptions)

	// Verify resources created by Terraform
	verifyTerraformResources(t, terraformOptions)

	// Destroy Terraform resources (assumed to succeed)
	terraform.Destroy(t, terraformOptions)
}

func verifyTerraformResources(t *testing.T, terraformOptions *terraform.Options) {
	// Verify specific resources created by Terraform (assumed to exist)
	clusterName := terraform.Output(t, terraformOptions, "cluster_name")
	assert.NotEmpty(t, clusterName, "cluster name shouldn't be empty")

	// Add more assertions as per your specific resource outputs
}